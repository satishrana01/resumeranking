# -*- coding: utf-8 -*-

import os
import warnings
import textract
import traceback
import extractEntities as entity
from gensim.summarization import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import jsonGetCategory as skills
from extract_exp import ExtractExp
from striprtf.striprtf import rtf_to_text
from pathlib import Path
import json
import boto3
from time import gmtime, strftime
import shutil

from functools import partial
import dask
from dask.diagnostics import ProgressBar
import numpy as np
import threading


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

global rootpath
global bucket_name
bucket_name = 'resume-rank-bucket' 
rootpath = "resume-rank-bucket"
global pathSeprator
pathSeprator = '/'

class ResultElement:
    def __init__(self, jd, filename,totalExp, phoneNo, email, exp,
                 finalRank,skills,nonTechskillList,min_qual,is_min_qual,candidateName,isJobTitlePresent,badWords):
        self.jd = jd
        self.filename = filename
        self.totalExp = totalExp
        self.phoneNo = phoneNo
        self.email = email
        self.exp = exp
        self.finalRank = finalRank
        self.primarySkills = skills
        self.softSkills = nonTechskillList
        self.min_qual =  min_qual
        self.is_min_qual = is_min_qual
        self.candidateName = candidateName
        self.isJobTitlePresent = isJobTitlePresent
        self.badWords = badWords
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp

def _s3_download(s3,bucket_name,path_to_read_file,i):
    try:
        s3.Bucket(bucket_name).download_file(i,path_to_read_file)
        
    except Exception as e:
        print(e)

def res(jobfile,skillset,jd_exp,min_qual, job_title,input_json,aws_path,must_have_skill, s3_resource, fs, bucket_name):
    is_min_qual = []
    Resume_skill_list = []
    Resume_non_skill_list = []
    Resume_email_vector = []
    Resume_phoneNo_vector = []
    Resume_total_exp_vector = []
    Resume_exp_vector = []
    Ordered_list_Resume = []
    LIST_OF_FILES = []
    LIST_OF_FILES_PDF = []
    LIST_OF_FILES_DOC = []
    LIST_OF_FILES_DOCX = []
    Resumes = []
    Temp_pdf = []
    badWords = []
    JD_rank_vector = []
    jd_rank_keyword = []
    
    jd_weightage = input_json["weightage"]["jd"]
    skill_weightage = input_json["weightage"]["skill"]
    min_qual_weightage = input_json["weightage"]["minimum_qualification"]
    non_tech_weightage = input_json["weightage"]["soft_skill"]
    
    exp_weightage = 0
    if (str(input_json["weightage"]["experience"]["required"]).lower() == 'true'):
        exp_weightage = input_json["weightage"]["experience"]["allocation"]
    
    not_found = 'Not Found'
    extract_exp = ExtractExp()
    s3 = boto3.resource('s3')
    root_path='temp/'
    resumePath = bucket_name+pathSeprator+aws_path+pathSeprator+'Upload-Resume'
        
    #print('length of resume list is ', len(resume_name_inS3))
    
    for file in fs.glob(resumePath+'/*.pdf'):
        LIST_OF_FILES_PDF.append(file)
    for file in fs.glob(resumePath+'/*.doc'):
        LIST_OF_FILES_DOC.append(file)
    for file in fs.glob(resumePath+'/*.docx'):
        LIST_OF_FILES_DOCX.append(file)
    for file in fs.glob(resumePath+'/*.rtf'):
        LIST_OF_FILES_DOCX.append(file)
    for file in fs.glob(resumePath+'/*.txt'):
        LIST_OF_FILES_DOCX.append(file)     

    LIST_OF_FILES = LIST_OF_FILES_DOC + LIST_OF_FILES_DOCX + LIST_OF_FILES_PDF
    # LIST_OF_FILES.remove("antiword.exe")
    print("Resume File list size ",len(LIST_OF_FILES))
    #pythoncom.CoInitialize()
    """ here we are creating the directory under temp folder"""
    sub_dir = aws_path.split(pathSeprator)[0]
    final_path = root_path+sub_dir+strftime("%H%M%S", gmtime())
    if not os.path.exists(final_path):
        os.makedirs(final_path)
        print("directory created",final_path)
    
    #download all files to local system
    dask.config.set(scheduler='threads', num_workers=20)
    _download = partial(_s3_download, s3,bucket_name)
    delayed_futures = []    
    for count,i in enumerate(LIST_OF_FILES):
        i = i.replace(bucket_name+pathSeprator, "")
        head, fileName = os.path.split(i)
        path_to_read_file = final_path+pathSeprator+fileName
        """_s3_download(s3,bucket_name,i,path_to_read_file)"""
        delayed_futures.append(dask.delayed(_download)(path_to_read_file,i))
    with ProgressBar():
        dask.compute(*delayed_futures)    
 
    for count,j in enumerate(LIST_OF_FILES):
       
        temp_path = j.rsplit('/',1)
        i = final_path+pathSeprator+temp_path[1]
        Temp = i.rsplit('.',-1)
        
        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                 with open(i,'rb') as pdf_file:
                    
                    read_pdf = PyPDF2.PdfFileReader(pdf_file,strict=False)
                    # page = read_pdf.getPage(0)
                    # page_content = page.extractText()
                    # Resumes.append(Temp_pdf)

                    number_of_pages = read_pdf.getNumPages()
                    for page_number in range(number_of_pages): 

                        page = read_pdf.getPage(page_number)
                        page_content = page.extractText()
                        page_content = page_content.replace('\n', ' ')
                        # page_content.replace("\r", "")
                        Temp_pdf = str(Temp_pdf) + str(page_content)
                        # Temp_pdf.append(page_content)
                        # print(Temp_pdf)
                    Resumes.extend([Temp_pdf])
                    Temp_pdf = ''
                    Ordered_list_Resume.append(i)
                    # f = open(str(i)+str("+") , 'w')
                    # f.write(page_content)
                    # f.close()
            except Exception as e: 
                print(e)
                print(traceback.format_exc())
        elif Temp[1] == "rtf" or Temp[1] == "Rtf" or Temp[1] == "RTF":
                
            try:
                
                rtf_path = Path(i)
                with rtf_path.open() as source:
                    docText = rtf_to_text(source.read())
                    
                c = [docText]
                Resumes.extend(c)
                Ordered_list_Resume.append(i)
            except Exception as e: print(e)
                
        elif Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            try:
                a = textract.process(i)
                a = a.replace(b'\n',  b' ')
                a = a.replace(b'\r',  b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
                Ordered_list_Resume.append(i)
                """try:
                    os.remove(path_to_read_file)
                except:
                    print ("unable to remove resume file ",path_to_read_file)
               """     
            except Exception as e: print(e)
            
        elif Temp[1] == "txt" or Temp[1] == "Txt" or Temp[1] == "TXT":
            try:
                f = open(i,'r')
                lines = f.readlines()
                a =  "\n".join(lines)
                c = [str(a)]
                Resumes.extend(c)
                Ordered_list_Resume.append(i)
                f.close()
            except Exception as e: print(e)    
                    
                
        elif Temp[1] == "ex" or Temp[1] == "Exe" or Temp[1] == "EXE":
            print("This is EXE" , i)
            pass
    print("final resume list are {}".format(len(Ordered_list_Resume)),end='\n')
    try:
        shutil.rmtree(final_path, ignore_errors=True)
    except:
        print("unable to delete directory ",final_path)

    flask_return = []
    print("Final list of resume",len(Ordered_list_Resume))
 
    for index,i in enumerate(Resumes):

        text = i
        temptext = str(text).lower()
        
        tttt = str(text).lower()
       
        
        try:
            if(skills.dndResume(temptext,must_have_skill)):
                continue
            try:
                tttt = summarize(tttt, word_count=100)
            except Exception:
                continue
            text = [tttt]
            jd_rankDict = skills.JDkeywordMatch(jobfile+skillset, temptext, jd_weightage)
            JD_rank_vector.append(jd_rankDict.get('rank'))
            jd_rank_keyword.append(jd_rankDict)
            
            badWords = skills.word_polarity(temptext)
            
            min_qual_score = skills.minQualificationScore(temptext,min_qual,min_qual_weightage)
            confidence = {}
            score = int((min_qual_score/min_qual_weightage)*100)
            confidence['confidence'] = score
            if score >= 60:
                confidence['min qual'] = 'Yes'
            elif score < 60 and score > 0:
                confidence['min qual'] = 'May Be'
            else:
                confidence['min qual'] = 'No'
            is_min_qual = confidence
            
            
            skill_rank = skills.programmingScore(temptext,jobfile+skillset,skill_weightage)
            Resume_skill_list = skills.skillSetListMatchedWithJD(temptext,jobfile+skillset,skill_rank)
            
            
            experience = extract_exp.get_features(temptext)
            Resume_total_exp_vector.append(experience)
            
            temp_applicantName = entity.extractPersonName(temptext, str(Ordered_list_Resume.__getitem__(index)))
                        
            bool_jobTitleFound = entity.isJobTitleAvailable(job_title, temptext)
                       
            temp_phone = entity.extract_phone_numbers(temptext)
            if(len(temp_phone) == 0):
                Resume_phoneNo_vector = not_found
            else:
                 Resume_phoneNo_vector = temp_phone
            temp_email = entity.extract_email_addresses(temptext)
            if(len(temp_email) == 0):
                Resume_email_vector = not_found
            else:
                 Resume_email_vector = temp_email
                
           
            Resume_exp_vector = extract_exp.get_exp_weightage(str(jd_exp),experience,exp_weightage)
            
            non_tech_Score = skills.NonTechnicalSkillScore(temptext,jobfile+skillset,non_tech_weightage)
            Resume_non_skill_list = skills.nonTechSkillSetListMatchedWithJD(temptext,jobfile+skillset,non_tech_Score)
            
            print("{} Rank prepared for {} ".format(index,Ordered_list_Resume.__getitem__(index)))
            
            file_path = resumePath+pathSeprator+Ordered_list_Resume.__getitem__(index).rsplit('/',1)[1]
            
            final_rating = jd_rankDict.get('rank')+skill_rank+non_tech_Score+extract_exp.get_exp_weightage(str(jd_exp),experience,exp_weightage)+min_qual_score
           
            res = ResultElement(jd_rankDict,file_path,experience,Resume_phoneNo_vector,Resume_email_vector,
                           Resume_exp_vector,round(final_rating),Resume_skill_list,
                           Resume_non_skill_list,min_qual_score,is_min_qual,temp_applicantName,bool_jobTitleFound,badWords)
            flask_return.append(res)
       
        except Exception:
            print(traceback.format_exc())
           
            
    return flask_return
