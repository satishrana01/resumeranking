import string
import os

global rootpath
rootpath = os.getcwd()
global pathSeprator
pathSeprator = '/'
global skill_threshold
skill_threshold = 5

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


def NonTechnicalSkillScore(resume, jd_txt,input_json):
    
    NonTechnicalSkill = loadSkillSetDB(rootpath+pathSeprator+"nonSkillDB.txt")
    programmingTotal = 0
    jdSkillCount = 0
    non_tech_weightage = input_json["weightage"]["soft_skill"]
    jdSkillMatched = []
    for i in range(len(NonTechnicalSkill)):
        if NonTechnicalSkill[i].lower() in jd_txt.lower() != -1:
            jdSkillCount += 1
            jdSkillMatched.append(NonTechnicalSkill[i].lower())
    if (jdSkillCount > 0):
        individualSkillWeightage = non_tech_weightage/jdSkillCount
    else :
        individualSkillWeightage = 0

    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            programmingTotal += 1
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
            
              
    resumeCorpus = resume.split()
    """ Modify below """
    resumeCorpus = resumeCorpus + ResumeProgrammingSkillsMatchedWithJD
    resumeCorpus = [x.lower() for x in resumeCorpus if isinstance(x, str)]
    jdSkillMatched = [x.lower() for x in jdSkillMatched if isinstance(x, str)]
    list1 = jdSkillMatched
    list2 = resumeCorpus
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

def dndResume(resumeText,must_have_skill):
    for skill in must_have_skill:
        if skill.lower() in resumeText:
            return False
        
    return True    