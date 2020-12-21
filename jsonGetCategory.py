import string
import os
from textblob import TextBlob

global rootpath
rootpath = os.getcwd()
global pathSeprator
pathSeprator = '/'
global skill_threshold
skill_threshold = 1

def programmingScore(resume, jdTxt,input_json):
    
    programming = loadSkillSetDB(rootpath+pathSeprator+"skillDB.txt")
    programmingTotal = 0
    skill_weightage = input_json["weightage"]["skill"]
    jdSkillMatched = []
    for i in range(len(programming)):
        if programming[i].lower() in jdTxt.lower() != -1:
            jdSkillMatched.append(programming[i].lower())
    jdSkillMatched = list(set(jdSkillMatched))
    individualSkillWeightage = 0
    
    if( len(jdSkillMatched) > 0):
        individualSkillWeightage = skill_weightage/len(jdSkillMatched)
    
    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            programmingTotal += 1
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
    
    list1 = []
    
    for item in ResumeProgrammingSkillsMatchedWithJD:
        list1.append(remove_punctuations(item))
    
    results = {}
    for i in list1:
        results[i] = 1
    
    results.update({n: individualSkillWeightage * results[n] for n in results.keys()})
    TotalScore = sum(results.values())
    
    return TotalScore

def word_polarity(resume_text):
    
    neg_word_list=[]

    for word in resume_text.split():               
        testimonial = TextBlob(word)
        if testimonial.sentiment.polarity <= -0.5:
            neg_word_list.append(word)
        
     
    return neg_word_list    

def minQualificationScore(resume, jdTxt,input_json):
    programming = loadSkillSetDB(rootpath+pathSeprator+"skillDB.txt")
    programmingTotal = 0
    min_qual_weightage = input_json["weightage"]["minimum_qualification"]
    jdSkillMatched = []
    for i in range(len(programming)):
        if programming[i].lower() in jdTxt.lower() != -1:
            #jdSkillCount += 1
            jdSkillMatched.append(programming[i].lower())
    jdSkillMatched = list(set(jdSkillMatched))
    individualSkillWeightage = 0
    
    if( len(jdSkillMatched) > 0):
        individualSkillWeightage = min_qual_weightage/len(jdSkillMatched)
    
    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            programmingTotal += 1
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
            #if not("#" in jdSkillMatched[i]):
                #fout.write(jdSkillMatched[i]+", ")
    resumeCorpus = resume.split()
    resumeCorpus = [x.lower() for x in resumeCorpus if isinstance(x, str)]
    jdSkillMatched = [x.lower() for x in jdSkillMatched if isinstance(x, str)]
    list1 = []
    for item in ResumeProgrammingSkillsMatchedWithJD:
        list1.append(remove_punctuations(item))
    list2 = []
    for item in resumeCorpus:
        list2.append(remove_punctuations(item))
    results = {}
    for i in list1:
        if list2.count(i) > skill_threshold:
            results[i] = skill_threshold
        else:
            results[i] = list2.count(i)
        
    constantValue = (individualSkillWeightage/skill_threshold)
    results.update({n: constantValue * results[n] for n in results.keys()})
    TotalScore = sum(results.values())
    
    return TotalScore

def skillSetListMatchedWithJD(resume, jdTxt,rank):
   
    programming = []
    programming = loadSkillSetDB(rootpath+pathSeprator+'skillDB.txt')
    jdSkillMatched = []
    skillMatched = []
    skillNotMatched = []
    finalResult ={}

    for i in range(len(programming)):
        if programming[i].lower() in jdTxt.lower() != -1:
            jdSkillMatched.append(programming[i].lower())
        
    
    jdSkillMatched = list(set(jdSkillMatched))
    
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            skillMatched.append(jdSkillMatched[i].lower())
        else:
            skillNotMatched.append(jdSkillMatched[i].lower())

    skillMatched = list(set(skillMatched))
    skillNotMatched = list(set(skillNotMatched))

    list1 = []
    list2 = []
    for item in skillMatched:
        list1.append(remove_punctuations(item))
        
    for item in skillNotMatched:
        list2.append(remove_punctuations(item))    

    finalResult['rank'] = round(rank)    
    finalResult['skillMatch'] = list1
    finalResult['skillUnMatch'] = list2
 
    return finalResult

def nonTechSkillSetListMatchedWithJD(resume, jdTxt,rank):
   
    programming = []
    programming = loadSkillSetDB(rootpath+pathSeprator+"nonSkillDB.txt")
    jdSkillMatched = []
    skillMatched = []
    skillUnMatched = []
    finalResult = {}
    for i in range(len(programming)):
        if programming[i].lower() in jdTxt.lower() != -1:
            jdSkillMatched.append(programming[i].lower())
    
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            skillMatched.append(jdSkillMatched[i].lower())
        else:
            skillUnMatched.append(jdSkillMatched[i].lower())

    skillMatched = list(set(skillMatched))
    skillUnMatched = list(set(skillUnMatched))
    
    finalResult['rank'] = round(rank)    
    finalResult['skillMatch'] = skillMatched
    finalResult['skillUnMatch'] = skillUnMatched
    
    return finalResult


def loadSkillSetDB(fileName):
    file = open(fileName,"r")
    skillDB = []
    for line in file:
        skillDB = line.split(",")
    file.close()
    return skillDB

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return ''.join(text)


def NonTechnicalSkillScore(resume, jd_txt,input_json):
    
    NonTechnicalSkill = loadSkillSetDB(rootpath+pathSeprator+"nonSkillDB.txt")
    non_tech_weightage = input_json["weightage"]["soft_skill"]
    if non_tech_weightage == 0:
        non_tech_weightage = 1
        
    jdSkillMatched = []
    for i in range(len(NonTechnicalSkill)):
        if NonTechnicalSkill[i].lower() in jd_txt.lower() != -1:
            jdSkillMatched.append(NonTechnicalSkill[i].lower())
    
    jdSkillMatched = list(set(jdSkillMatched))
    
    if (len(jdSkillMatched) > 0):
        individualSkillWeightage = non_tech_weightage/len(jdSkillMatched)
    else :
        individualSkillWeightage = 0

    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
            
    results = {}
    for i in ResumeProgrammingSkillsMatchedWithJD:
        results[i] = 1
 		
    results.update({n: individualSkillWeightage * results[n] for n in results.keys()})
    TotalScore = sum(results.values())
    
    return TotalScore

def dndResume(resumeText,must_have_skill):
    for skill in must_have_skill:
        if skill.lower() in resumeText:
            return False
        
    return True    