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

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

global rootpath
global bucket_name
bucket_name = 'resume-rank-bucket' 
rootpath = "resume-rank-bucket"
global pathSeprator
pathSeprator = '/'
global skill_threshold
skill_threshold = 5
global exp_weightage
exp_weightage = 30


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
   
def res(jobfile,skillset,jd_exp,min_qual, job_title,input_json,aws_path,must_have_skill, s3_resource, fs, bucket_name):
    Resume_Vector = []
    Resume_skill_vector = []
    min_qual_vector = []
    is_min_qual = []
    Resume_skill_list = []
    Resume_non_skill_list = []
    Resume_email_vector = []
    Resume_JobTitleAvailability_vector = []
    Resume_phoneNo_vector = []
    Resume_ApplicantName_vector = []
    Resume_total_exp_vector = []
    Resume_nonTechSkills_vector = []
    Resume_exp_vector = []
    Ordered_list_Resume = []
    LIST_OF_FILES = []
    LIST_OF_FILES_PDF = []
    LIST_OF_FILES_DOC = []
    LIST_OF_FILES_DOCX = []
    Resumes = []
    Temp_pdf = []
    Resume_title = []
    badWords = []
    JD_rank_vector = []
    jd_rank_keyword = []
    jd_weightage = input_json["weightage"]["jd"]
    not_found = 'Not Found'
    extract_exp = ExtractExp()
    s3 = boto3.resource('s3')
    root_path='temp/'
    resumePath = bucket_name+pathSeprator+aws_path+pathSeprator+'Upload-Resume'
    
    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.all():
        if '{}/'.format(resumePath) in obj.key:
            #print(obj.key)
            Temp = obj.key.split('/',-1)
            #print(Temp)
            Resume_title = Resume_title + [Temp[-1]]
        
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
    print("Resume File list",LIST_OF_FILES)
    #pythoncom.CoInitialize()
    """ here we are creating the directory under temp folder"""
    sub_dir = aws_path.split(pathSeprator)[0] 
    final_path = root_path+sub_dir+strftime("%H%M%S", gmtime())
    if not os.path.exists(final_path):
        os.makedirs(final_path)
        print("directory created",final_path)
        
    for count,i in enumerate(LIST_OF_FILES):
       
        Temp = i.rsplit('.',-1)
        #rr= Temp[0].rsplit('/',1)
        
        #Resume_title.append(rr[-1])
        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                with fs.open(i,'rb') as pdf_file:
                    
                    read_pdf = PyPDF2.PdfFileReader(pdf_file)
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
        elif Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":
            print(count," This is DOC" , i)
                
            #parse_docfile(i)
         
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
                i = i.replace(bucket_name+pathSeprator, "")
                head, fileName = os.path.split(i)
                path_to_read_file = final_path+pathSeprator+fileName
                s3.Bucket(bucket_name).download_file(i,path_to_read_file)
                a = textract.process(path_to_read_file)
                a = a.replace(b'\n',  b' ')
                a = a.replace(b'\r',  b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
                Ordered_list_Resume.append(i)
                try:
                    os.remove(path_to_read_file)
                except:
                    print ("unable to remove resume file ",path_to_read_file)
            except Exception as e: print(e)
            
        elif Temp[1] == "txt" or Temp[1] == "Txt" or Temp[1] == "TXT":
            try:
                f = fs.open(i,'r')
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
    print("final resume list are {} and {}".format(len(Ordered_list_Resume), Ordered_list_Resume),end='\n')
    print("Cv's Done Parsing.",end='\n')
    print("Please wait we are preparing ranking.",end='\n')
    #os.rmdir(final_path)
    try:
        shutil.rmtree(final_path, ignore_errors=True)
    except:
        print("unable to delete directory ",final_path)

    Job_Desc = 0
    
    try:
        tttt = str(jobfile)
        JDText = tttt
        tttt = summarize(tttt, word_count=100)
        text = [tttt]
    except:
        text = 'None'

    
    vectorizer = TfidfVectorizer(stop_words='english')
    # print(text)
    vectorizer.fit(text)
    vector = vectorizer.transform(text)

    Job_Desc = vector.toarray()
    tempList = Ordered_list_Resume 
    flask_return = []
    for index,i in enumerate(Resumes):

        text = i
        temptext = str(text).lower()
        tttt = str(text).lower()
       
        
        try:
            if(skills.dndResume(temptext,must_have_skill)):
                continue
            tttt = summarize(tttt, word_count=100) 
            text = [tttt]
            vector = vectorizer.transform(text)
            Resume_Vector.append(vector.toarray())
            min_qual_score = skills.minQualificationScore(temptext,min_qual,input_json)
            jd_rankDict = skills.JDkeywordMatch(jobfile+skillset, temptext, jd_weightage)
            JD_rank_vector.append(jd_rankDict.get('rank'))
            jd_rank_keyword.append(jd_rankDict)
            badWords.append(skills.word_polarity(temptext))
            min_qual_vector.append(min_qual_score)
            confidence = {}
            score = int((min_qual_score/input_json["weightage"]["minimum_qualification"])*100)
            confidence['confidence'] = score
            if score >= 60:
                confidence['min qual'] = 'Yes'
            elif score < 60 and score > 0:
                confidence['min qual'] = 'May Be'
            else:
                confidence['min qual'] = 'No'
            is_min_qual.append(confidence)
            skill_rank = skills.programmingScore(temptext,jobfile+skillset,input_json)
            Resume_skill_vector.append(skill_rank)
            Resume_skill_list.append(skills.skillSetListMatchedWithJD(temptext,jobfile+skillset,skill_rank))
            experience = extract_exp.get_features(temptext)
            Resume_total_exp_vector.append(experience)
            temp_applicantName = entity.extractPersonName(temptext, str(Ordered_list_Resume.__getitem__(index)))
            Resume_ApplicantName_vector.append(temp_applicantName)
            bool_jobTitleFound = entity.isJobTitleAvailable(job_title, temptext)
            Resume_JobTitleAvailability_vector.append(bool_jobTitleFound)
            temp_phone = entity.extract_phone_numbers(temptext)
            if(len(temp_phone) == 0):
                Resume_phoneNo_vector.append(not_found)
            else:
                 Resume_phoneNo_vector.append(temp_phone)
            temp_email = entity.extract_email_addresses(temptext)
            if(len(temp_email) == 0):
                Resume_email_vector.append(not_found)
            else:
                 Resume_email_vector.append(temp_email)
                
           
            Resume_exp_vector.append(extract_exp.get_exp_weightage(str(jd_exp),experience))
            non_tech_Score = skills.NonTechnicalSkillScore(temptext,jobfile+skillset,input_json)
            Resume_nonTechSkills_vector.append(non_tech_Score)
            Resume_non_skill_list.append(skills.nonTechSkillSetListMatchedWithJD(temptext,jobfile+skillset,non_tech_Score))
            
            print("Rank prepared for ",Ordered_list_Resume.__getitem__(index))
        except Exception:
            print(traceback.format_exc())
            tempList.__delitem__(index)
            
   # Resume_JobTitleAvailability_vector.__getitem__(index)
    for index,i in enumerate(Resume_Vector):

        samples = i
        #similarity = cosine_similarity(samples,Job_Desc)[0][0]
        """Ordered_list_Resume_Score.extend(similarity)"""
        final_rating = JD_rank_vector.__getitem__(index)+Resume_skill_vector.__getitem__(index)+Resume_nonTechSkills_vector.__getitem__(index)+Resume_exp_vector.__getitem__(index)+min_qual_vector.__getitem__(index)
        res = ResultElement(jd_rank_keyword.__getitem__(index),tempList.__getitem__(index),
                           Resume_total_exp_vector.__getitem__(index), Resume_phoneNo_vector.__getitem__(index),Resume_email_vector.__getitem__(index),
                           Resume_exp_vector.__getitem__(index),round(final_rating),Resume_skill_list.__getitem__(index),
                           Resume_non_skill_list.__getitem__(index),min_qual_vector.__getitem__(index),is_min_qual.__getitem__(index),Resume_ApplicantName_vector.__getitem__(index),Resume_JobTitleAvailability_vector.__getitem__(index),badWords.__getitem__(index))
        flask_return.append(res)
        #print(res.toJSON())
    #flask_return.sort(key=lambda x: x.finalRank, reverse=True)
    #flask_return = [word.replace('\n    ','') for word in flask_return]
    return flask_return

