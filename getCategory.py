import string
import globals
import os

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

def programmingScore(resume, jdTxt):
    
    programming = loadSkillSetDB(rootpath+pathSeprator+"skillDB.txt")
    programmingTotal = 0
    
    #jdSkillCount = 0
    jdSkillMatched = []
    for i in range(len(programming)):
        if programming[i].lower() in jdTxt.lower() != -1:
            #jdSkillCount += 1
            jdSkillMatched.append(programming[i].lower())
    #print("jdSkillCount", jdSkillCount)
    #for x in range(len(jdSkillMatched)): 
    #print("jd Skills matched are ",jdSkillMatched)
    #END 
    jdSkillMatched = list(set(jdSkillMatched))
    individualSkillWeightage = 0
    
    if( len(jdSkillMatched) > 0):
        individualSkillWeightage = skill_weightage/len(jdSkillMatched)
    
    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            programmingTotal += 1
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
            #if not("#" in jdSkillMatched[i]):
                #fout.write(jdSkillMatched[i]+", ")
    #print("Resume skills matched with JD are ", ResumeProgrammingSkillsMatchedWithJD)
    #print("programming total is ", programmingTotal)
    
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
        
    #print("Dictionary is ",results)
    #print(list1)
    #print("list2",list2)
    
    #print(results)
   #end of code
   
    constantValue = (individualSkillWeightage/skill_threshold)
    #print("constant",constantValue)
    # Updating Dictionary
    results.update({n: constantValue * results[n] for n in results.keys()})
    #print("updated dict is ", results)
    #print("updated dict",results)
    TotalScore = sum(results.values())
    #print("Score is ", TotalScore)

    #fout.close()

    #progScore = min(programmingTotal/10.0, 1) * 5.0


    return TotalScore

def minQualificationScore(resume, jdTxt):
    programming = loadSkillSetDB(rootpath+pathSeprator+"skillDB.txt")
    programmingTotal = 0
    
    #jdSkillCount = 0
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

def skillSetListMatchedWithJD(resume, jdTxt):
   
    programming = []
    programming = loadSkillSetDB(rootpath+pathSeprator+'skillDB.txt')
    jdSkillCount = 0
    jdSkillMatched = []
    skillMatched = []
    results = {}
    for i in range(len(programming)):
        if programming[i].lower() in jdTxt.lower() != -1:
            jdSkillCount += 1
            jdSkillMatched.append(programming[i].lower())
    
    jdSkillMatched = list(set(jdSkillMatched))
    
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            skillMatched.append(jdSkillMatched[i].lower())
            

    #print(skillMatched)
    skillMatched = list(set(skillMatched))
    resumeCorpus = resume.split()
    resumeCorpus = [x.lower() for x in resumeCorpus if isinstance(x, str)]
    list1 = []
    for item in skillMatched:
        list1.append(remove_punctuations(item))
    list2 = []
    for item in resumeCorpus:
        list2.append(remove_punctuations(item))
    results = {}
    for i in list1:
        results[i] = list2.count(i)
    
    return results

def nonTechSkillSetListMatchedWithJD(resume, jdTxt):
   
    programming = []
    programming = loadSkillSetDB(rootpath+pathSeprator+"nonSkillDB.txt")
    jdSkillCount = 0
    jdSkillMatched = []
    skillMatched = []
    for i in range(len(programming)):
        if programming[i].lower() in jdTxt.lower() != -1:
            jdSkillCount += 1
            jdSkillMatched.append(programming[i].lower())
    
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            skillMatched.append(jdSkillMatched[i].lower())

    #print(skillMatched)
    skillMatched = list(set(skillMatched))
    return skillMatched


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


def NonTechnicalSkillScore(resume, jd_txt):
    
    NonTechnicalSkill = loadSkillSetDB(rootpath+pathSeprator+"nonSkillDB.txt")
    programmingTotal = 0
    
    # ADDED BY SAURABH for extracting JD skills is *WORKING* 
    jdSkillCount = 0
    jdSkillMatched = []
    for i in range(len(NonTechnicalSkill)):
        if NonTechnicalSkill[i].lower() in jd_txt.lower() != -1:
            jdSkillCount += 1
            jdSkillMatched.append(NonTechnicalSkill[i].lower())
    #print("jdSkillCount", jdSkillCount)
    #for x in range(len(jdSkillMatched)): 
    #print("jd Skills matched are ",jdSkillMatched)
    #END 
    if (jdSkillCount > 0):
        individualSkillWeightage = non_tech_weightage/jdSkillCount
    else :
        individualSkillWeightage = 0

    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            programmingTotal += 1
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
            #if not("#" in jdSkillMatched[i]):
                #fout.write(jdSkillMatched[i]+", ")
    #print("Resume skills matched with JD are ", ResumeProgrammingSkillsMatchedWithJD)
    #print("Non Technical skill total is ", programmingTotal)
    
   # My Code 
    resumeCorpus = resume.split()
    """ Modify below """
    resumeCorpus = resumeCorpus + ResumeProgrammingSkillsMatchedWithJD
    resumeCorpus = [x.lower() for x in resumeCorpus if isinstance(x, str)]
    jdSkillMatched = [x.lower() for x in jdSkillMatched if isinstance(x, str)]
    #print(type(resumeCorpus))
    #print("jd skills matched in lower case",jdSkillMatched)
    list1 = jdSkillMatched
    list2 = resumeCorpus
    results = {}
    for i in list1:
        if list2.count(i) > skill_threshold:
           results[i] = skill_threshold
        else:
           results[i] = list2.count(i)
		
    #print("Relevant non-technical skills and their count in resume as per the JD are below")
    #print("Dictionary from resume is ",results)
    #print(type(results))
   #end of code
   
    constantValue = (individualSkillWeightage/skill_threshold)
    # Updating Dictionary
    results.update({n: constantValue * results[n] for n in results.keys()})
    TotalScore = sum(results.values())
    #fout.close()

    #progScore = min(programmingTotal/10.0, 1) * 5.0


    return TotalScore
