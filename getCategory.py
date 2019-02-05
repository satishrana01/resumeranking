import re
import string
import globals

def programmingScore(resume, jdTxt):
    skill_weightage = 40
    skill_threshold = 5
    fout = open("results.tex", "a")
    fout.write("\\textbf{Programming Languages:} \\\\\n")
    programming = loadSkillSetDB(globals.rootpath+globals.pathSeprator+"skillDB.txt")
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
            if not("#" in jdSkillMatched[i]):
                fout.write(jdSkillMatched[i]+", ")
    print("Resume skills matched with JD are ", ResumeProgrammingSkillsMatchedWithJD)
    #print("programming total is ", programmingTotal)
    
   # My Code 
    resumeCorpus = resume.split()
    resumeCorpus = [x.lower() for x in resumeCorpus if isinstance(x, str)]
    jdSkillMatched = [x.lower() for x in jdSkillMatched if isinstance(x, str)]
    list1 = ResumeProgrammingSkillsMatchedWithJD
    list2 = []
    for item in resumeCorpus:
        list2.append(remove_punctuations(item))
    results = {}
    for i in list1:
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

    fout.close()

    #progScore = min(programmingTotal/10.0, 1) * 5.0


    return TotalScore

def skillSetListMatchedWithJD(resume, jdTxt):
   
    programming = []
    programming = loadSkillSetDB(globals.rootpath+globals.pathSeprator+'skillDB.txt')
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

def nonTechSkillSetListMatchedWithJD(resume, jdTxt):
   
    programming = []
    programming = loadSkillSetDB(globals.rootpath+globals.pathSeprator+"nonSkillDB.txt")
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
    skill_weightage = 5
    skill_threshold = 5
    fout = open("results.tex", "a")
    fout.write("\\textbf{Programming Languages:} \\\\\n")
    NonTechnicalSkill = loadSkillSetDB(globals.rootpath+globals.pathSeprator+"nonSkillDB.txt")
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
        individualSkillWeightage = skill_weightage/jdSkillCount
    else :
        individualSkillWeightage = 0

    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            programmingTotal += 1
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
            if not("#" in jdSkillMatched[i]):
                fout.write(jdSkillMatched[i]+", ")
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
    fout.close()

    #progScore = min(programmingTotal/10.0, 1) * 5.0


    return TotalScore
