#import pythoncom
import glob
import os
import warnings
import textract
#from win32com.client import Dispatch
import traceback
import extractEntities as entity
from gensim.summarization import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import getCategory as skills
from extract_exp import ExtractExp
from striprtf.striprtf import rtf_to_text
from pathlib import Path
import pandas as pd

os.chdir('Upload-JD')
ffile = glob.glob('*.xlsx', recursive=False)
job_data_set = pd.read_excel(ffile[0])
job_title = job_data_set['Job Title'][0]
print("Job title is {}".format(job_title))
os.chdir('..')

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

global rootpath
rootpath = os.getcwd()
global pathSeprator
pathSeprator = '/'
global min_qual_weightage
min_qual_weightage = 15
global skill_threshold
skill_threshold = 5
global non_tech_weightage
non_tech_weightage = 5
global exp_weightage
exp_weightage = 30
global skill_weightage
skill_weightage = 35

class ResultElement:
    def __init__(self, jd, filename,skillRank, totalExp, phoneNo, email, nonTechSkills,exp,
                 finalRank,skillList,nonTechskillList,min_qual,is_min_qual,candidateName):
        self.jd = jd
        self.filename = filename
        self.skillRank = skillRank
        self.totalExp = totalExp
        self.phoneNo = phoneNo
        self.email = email
        self.nonTechSkills = nonTechSkills
        self.exp = exp
        self.finalRank = finalRank
        self.skillList = skillList
        self.nonTechskillList = nonTechskillList
        self.min_qual =  min_qual
        self.is_min_qual = is_min_qual
        self.candidateName = candidateName

def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp
"""
def parse_docfile(file):
    pythoncom.CoInitialize()
    wordapp = Dispatch("Word.Application")
    doc = wordapp.Documents.Open(os.getcwd()+"/"+file)
    docText = doc.Content.Text
    wordapp.Quit()
    return docText
"""    
def res(jobfile,skillset,jd_exp,min_qual):
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
    #if count == 0:
    #    os.chdir("..")
    #    print(os.getcwd())
    #    os.chdir('Upload-Resume')
    jd_weightage = 15
    not_found = 'Not Found'
    extract_exp = ExtractExp()
    
    resumePath = rootpath+pathSeprator+'Upload-Resume'
    
    for file in glob.glob(resumePath+'/*.pdf'):
        LIST_OF_FILES_PDF.append(file)
    for file in glob.glob(resumePath+'/*.doc'):
        LIST_OF_FILES_DOC.append(file)
    for file in glob.glob(resumePath+'/*.docx'):
        LIST_OF_FILES_DOCX.append(file)
    for file in glob.glob(resumePath+'/*.rtf'):
        LIST_OF_FILES_DOCX.append(file)
    for file in glob.glob(resumePath+'/*.txt'):
        LIST_OF_FILES_DOCX.append(file)     

    LIST_OF_FILES = LIST_OF_FILES_DOC + LIST_OF_FILES_DOCX + LIST_OF_FILES_PDF
    # LIST_OF_FILES.remove("antiword.exe")
    print("This is LIST OF FILES")
    print(LIST_OF_FILES)

    
    print("####### PARSING ########")
    #pythoncom.CoInitialize()
    
    for count,i in enumerate(LIST_OF_FILES):
       
        Temp = i.rsplit('.', 1)
        rr= Temp[0].rsplit('\\', 1)
        
        print("rr is {}".format(rr[-1]))
        Resume_title.append(rr[-1])
        print("Resume title is {}".format(Resume_title))
        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                print(count," This is PDF" , i)
                with open(i,'rb') as pdf_file:
                    
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
            print(count," This is Rtf" , i)
                
            try:
                
                rtf_path = Path(i)
                with rtf_path.open() as source:
                    docText = rtf_to_text(source.read())
                    
                c = [docText]
                Resumes.extend(c)
                Ordered_list_Resume.append(i)
            except Exception as e: print(e)
                
        elif Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            print(count," This is DOCX" , i)
            try:
                a = textract.process(i)
                a = a.replace(b'\n',  b' ')
                a = a.replace(b'\r',  b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
                Ordered_list_Resume.append(i)
            except Exception as e: print(e)
            
        elif Temp[1] == "txt" or Temp[1] == "Txt" or Temp[1] == "TXT":
            print(count," This is txt" , i)
            try:
                f = open(file,'r')
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

    print("Done Parsing.")
    print("Please wait we are preparing ranking.")

    Job_Desc = 0
    
    try:
        tttt = str(jobfile)
        tttt = summarize(tttt, word_count=100)
        text = [tttt]
    except:
        text = 'None'

    
    vectorizer = TfidfVectorizer(stop_words='english')
    # print(text)
    vectorizer.fit(text)
    vector = vectorizer.transform(text)

    Job_Desc = vector.toarray()
    # print("\n\n")
    # print("This is job desc : " , Job_Desc)
    tempList = Ordered_list_Resume 
    os.chdir('../')
    flask_return = []
    for index,i in enumerate(Resumes):

        text = i
        temptext = str(text)
        tttt = str(text)
       
        
        try:
            tttt = summarize(tttt, word_count=100) 
            text = [tttt]
            vector = vectorizer.transform(text)
            Resume_Vector.append(vector.toarray())
            min_qual_score = skills.minQualificationScore(temptext,min_qual)
            min_qual_vector.append(min_qual_score)
            confidence = {}
            score = int((min_qual_score/min_qual_weightage)*100)
            confidence['confidence'] = score
            if score >= 60:
                confidence['min qual'] = 'Yes'
            elif score < 60 and score > 0:
                confidence['min qual'] = 'May Be'
            else:
                confidence['min qual'] = 'No'
            is_min_qual.append(confidence)
            Resume_skill_vector.append(skills.programmingScore(temptext,jobfile+skillset))
            Resume_skill_list.append(skills.skillSetListMatchedWithJD(temptext,jobfile+skillset))
            Resume_non_skill_list.append(skills.nonTechSkillSetListMatchedWithJD(temptext,jobfile+skillset))
            experience = extract_exp.get_features(temptext)
            Resume_total_exp_vector.append(experience)
            temp_applicantName = entity.extractPersonName(temptext, str(Resume_title.__getitem__(index)))
            Resume_ApplicantName_vector.append(temp_applicantName)
            bool_jobTitleFound = entity.isJobTitleAvailable(jobTitle, temptext)
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
            Resume_nonTechSkills_vector.append(skills.NonTechnicalSkillScore(temptext,jobfile+skillset))
            print("Rank prepared for ",Ordered_list_Resume.__getitem__(index))
        except Exception:
            print(traceback.format_exc())
            tempList.__delitem__(index)
            
   
    for index,i in enumerate(Resume_Vector):

        samples = i
        similarity = cosine_similarity(samples,Job_Desc)[0][0]
        """Ordered_list_Resume_Score.extend(similarity)"""
        #print(Resume_skill_vector)
        #print(Resume_nonTechSkills_vector)
        #print(Resume_exp_vector)
        final_rating = round(similarity*jd_weightage,2)+Resume_skill_vector.__getitem__(index)+Resume_nonTechSkills_vector.__getitem__(index)+Resume_exp_vector.__getitem__(index)
        res = ResultElement(round(similarity*jd_weightage,2), os.path.basename(tempList.__getitem__(index)),round(Resume_skill_vector.__getitem__(index),2),
                           Resume_total_exp_vector.__getitem__(index), Resume_phoneNo_vector.__getitem__(index),Resume_email_vector.__getitem__(index),
                           Resume_JobTitleAvailability_vector.__getitem__(index), Resume_nonTechSkills_vector.__getitem__(index),Resume_exp_vector.__getitem__(index),round(final_rating,2),Resume_skill_list.__getitem__(index),
                           Resume_non_skill_list.__getitem__(index),min_qual_vector.__getitem__(index),is_min_qual.__getitem__(index),Resume_ApplicantName_vector.__getitem__(index))
        flask_return.append(res)
    flask_return.sort(key=lambda x: x.finalRank, reverse=True)
    return flask_return
 
