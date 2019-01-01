import pythoncom
import glob
import os
import warnings
import textract
import weightage_program as exp
import win32com.client
import traceback
import extractEntities as entity
from gensim.summarization import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import getCategory as skills


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')




class ResultElement:
    def __init__(self, jd, filename,skillRank, name, phoneNo, email, nonTechSkills,exp,finalRank):
        self.jd = jd
        self.filename = filename
        self.skillRank = skillRank
        self.name = name
        self.phoneNo = phoneNo
        self.email = email
        self.nonTechSkills = nonTechSkills
        self.exp = exp
        self.finalRank = finalRank


def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp


def res(jobfile,skillset,jd_exp):
    Resume_Vector = []
    Resume_skill_vector = []
    Resume_email_vector = []
    Resume_phoneNo_vector = []
    Resume_name_vector = []
    Resume_nonTechSkills_vector = []
    Resume_exp_vector = []
    Ordered_list_Resume = []
    LIST_OF_FILES = []
    LIST_OF_FILES_PDF = []
    LIST_OF_FILES_DOC = []
    LIST_OF_FILES_DOCX = []
    Resumes = []
    Temp_pdf = []
    os.chdir("..")
    print(os.getcwd())
    os.chdir('Upload-Resume')
    jd_weightage = 15
    
    
    for file in glob.glob('**/*.pdf', recursive=True):
        LIST_OF_FILES_PDF.append(file)
    for file in glob.glob('**/*.doc', recursive=True):
        LIST_OF_FILES_DOC.append(file)
    for file in glob.glob('**/*.docx', recursive=True):
        LIST_OF_FILES_DOCX.append(file)

    LIST_OF_FILES = LIST_OF_FILES_DOC + LIST_OF_FILES_DOCX + LIST_OF_FILES_PDF
    # LIST_OF_FILES.remove("antiword.exe")
    print("This is LIST OF FILES")
    print(LIST_OF_FILES)

    # print("Total Files to Parse\t" , len(LIST_OF_PDF_FILES))
    print("####### PARSING ########")
    for nooo,i in enumerate(LIST_OF_FILES):
       
        Temp = i.rsplit('.', 1)
        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                print("This is PDF" , nooo)
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
        if Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":
            print("This is DOC" , i)
                
            try:
                pythoncom.CoInitialize()
                wordapp = win32com.client.Dispatch("Word.Application")
                doc = wordapp.Documents.Open(os.getcwd()+"/"+i)
                docText = doc.Content.Text
                wordapp.Quit()
                c = [docText]
                Resumes.extend(c)
                Ordered_list_Resume.append(i)
            except Exception as e: print(e)
                
                
        if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            print("This is DOCX" , i)
            try:
                a = textract.process(i)
                a = a.replace(b'\n',  b' ')
                a = a.replace(b'\r',  b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
                Ordered_list_Resume.append(i)
            except Exception as e: print(e)
                    
                
        if Temp[1] == "ex" or Temp[1] == "Exe" or Temp[1] == "EXE":
            print("This is EXE" , i)
            pass



    print("Done Parsing.")



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
            Resume_skill_vector.append(skills.programmingScore(temptext,jobfile+skillset))
            Resume_email_vector.append(entity.extract_email_addresses(temptext))
            Resume_name_vector.append(entity.extract_name(temptext))
            Resume_phoneNo_vector.append(entity.extract_phone_numbers(temptext))
            Resume_exp_vector.append(exp.get_exp(jd_exp,temptext))
            Resume_nonTechSkills_vector.append(skills.NonTechnicalSkillScore(temptext,jobfile+skillset))
        except Exception:
            print(traceback.format_exc())
            tempList.__delitem__(index)
            
   
    for index,i in enumerate(Resume_Vector):

        samples = i
        similarity = cosine_similarity(samples,Job_Desc)[0][0]
        """Ordered_list_Resume_Score.extend(similarity)"""
        print(Resume_skill_vector)
        print(Resume_nonTechSkills_vector)
        print(Resume_exp_vector)
        final_rating = round(similarity*jd_weightage,2)+Resume_skill_vector.__getitem__(index)+Resume_nonTechSkills_vector.__getitem__(index)+Resume_exp_vector.__getitem__(index)
        res = ResultElement(round(similarity*jd_weightage,2), tempList.__getitem__(index),Resume_skill_vector.__getitem__(index),
                           Resume_name_vector.__getitem__(index),Resume_phoneNo_vector.__getitem__(index),Resume_email_vector.__getitem__(index),
                           Resume_nonTechSkills_vector.__getitem__(index),Resume_exp_vector.__getitem__(index),round(final_rating,2))
        flask_return.append(res)
    flask_return.sort(key=lambda x: x.finalRank, reverse=True)
    return flask_return
    # for n,i in enumerate(Z):
    #     print("Rankkkkk\t" , n+1, ":\t" , i)

    """for n,i in enumerate(Z):
        # print("Rank\t" , n+1, ":\t" , i)
        # flask_return.append(str("Rank\t" , n+1, ":\t" , i))
        name = getfilepath(i)
        #name = name.split('.')[0]
        rank = n+1
        res = ResultElement(rank, name)
        flask_return.append(res)
        # res.printresult()
        print(f"Rank{res.rank+1} :\t {res.filename}")
    return flask_return"""


if __name__ == '__main__':
    inputStr = input("")
    sear(inputStr)

