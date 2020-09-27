# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 20:57:57 2018

@author: saurabh.keshari
"""
#python -m spacy download en_core_web_sm
#mport spacy
import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import wordnet
from text_process import remove_stopwords, to_lowercase

#from collections import Counter
#import en_core_web_sm


#Function to extract names from the string using spacy
def extract_name(resume):
   
   # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = en_core_web_sm.load()
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(resume)
    for ent in doc.ents:
        if(ent.label_ == 'PER'):
            print(ent.text)
            break 
    return ent.text                  

#Function to extract Phone Numbers from string using regular expressions
def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers if len(number) >9]

#Function to extract Email address from a string using regular expressions
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def extractPersonName(tttt, resumeTitle):
        #a = 'Cv_saurabh+keshari_1234_Resume'
        #a = "1234"
        print("resume title is {} and type is {}".format(resumeTitle, type(resumeTitle)))
        titleSplit = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', resumeTitle)
        title_isNotDigit = []
        for word in titleSplit:
            if not word.isdigit():
                title_isNotDigit.append(word)
        strr = " ".join(title_isNotDigit)
        strr_list = strr.split(" ")
        #titleSplit = re.findall(r"[\w']+", strr)
        
        Names = []
        for Nouns in strr_list:
            if not wordnet.synsets(Nouns):
                #Not an English word
                Names.append(Nouns)
        titleSplit_lower = to_lowercase(Names)
        titleSplit_cleaned = remove_stopwords(titleSplit_lower)
        personName = "ABC"
        if len(titleSplit_cleaned) > 0:
            print('within if')
            if len(titleSplit_cleaned) == 1:
                firstName = titleSplit_cleaned[0]
                personName = firstName
            if len(titleSplit_cleaned) == 2: 
                firstName = titleSplit_cleaned[0]
                secondName = titleSplit_cleaned[1]
                personName = firstName +" " + secondName
            if len(titleSplit_cleaned) >= 3: 
                firstName = titleSplit_cleaned[0]
                secondName = titleSplit_cleaned[1]
                thirdName = titleSplit_cleaned[2]
                personName = firstName +" " + secondName
        
        else:
            print("within else")
            TITLE = r"(?:[A-Z][a-z]*\.\s*)?"
            NAME1 = r"[A-Z][a-z]+,?\s+"
            MIDDLE_I = r"(?:[A-Z][a-z]*\.?\s*)?"
            NAME2 = r"[A-Z][a-z]+"
            name = []
            name = re.findall(TITLE + NAME1 + MIDDLE_I + NAME2, tttt)
            if len(name) > 0:
                rep1 = {"Career": "", "career": "", "Objective":"", "objective": "", "Email": "", "email": "", "Experience Summary": "", "ph": "", "Ph": "", "Professional": "", "Curriculum Vitae": "", "Resume": "", "Profile": "", "Professional": "", "Recruiter": "", "Lead": "", "Summary": "", "HR": "", "new":"", "New": ""}  # define desired replacements here
                rep = dict((re.escape(k), v) for k, v in rep1.items()) 
                #Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
                pattern = re.compile("|".join(rep.keys()))
                personName = pattern.sub(lambda m: rep[re.escape(m.group(0))], name[0])
            else:  
                personName = "No name found"
         
        stopwords = ['HR', 'hr','pdf', 'xls', 'docx', 'doc', 'rtf', 'txt', "assembly", "bash", " c " "c++", "c#", "coffeescript", "emacs lisp",
         "go!", "groovy", "haskell", "java", "javascript", "matlab", "max MSP", "objective c", "qlikview", "crm", "CRM", "dynamics",
         "perl", "php","html", "xml", "css", "processing", "python", "ruby", "sml", "swift", "resume","Resume",
         "latex" "unity", "unix" "visual basic" "wolfram language", "xquery", "sql", "node.js", "finance", "liferay",
         "scala", "kdb", "jquery", "mongodb", "CMMI", "ISO", "finance", "Banking", "Finacle", "Oracle Flexcube", "Fiserv", "successfactor", "sf", "success factor", "Success Factor",
         "TCS BaNcs", "FIS Profile", "Self-directed learning", "Collaboration", "Communication", "Resilience", "Big-picture mindset", "Prioritization ", "Creativity ",
         "creative", "Insight", "curiosity", "curious", "Openness", "Teamwork", "Time management", "Emotional intelligence", 
         "quick learner", "problem solver","Customer-service skills", "Planning and organizing", "innovative", "Thinking innovatively and creatively", "Resourceful", "Flexible", "Able to manage own time", "Having self-esteem", 
         "Innovation skills", "Enterprise skills", "Civic or citizenship knowledge and skills", "Sociability", "Self-management", "Integrity", "Honesty", "Human resources", 
         "Participates as a team member", "Works with diversity", "Exercises leadership", "leadership", "Exercises leadership", "Monitors and corrects performance", "Understands systems", 'experience', 'exp', 'exp.']
        querywords = personName.split()
        
        resultwords  = [word for word in querywords if word.lower() not in stopwords]
        result = ' '.join(resultwords)         
        return result

"""

resume = open("resumeSample.txt", "r")
resume_txt = resume.read()
#print(resume_txt)
#print(programmingScore(pdftotextmaybe.convert("Sample resumes/sample1.pdf"), jd_txt) )
#print(extract_name(resume_txt) )
print("Phone numbers are ",extract_phone_numbers(resume_txt) )
print("Email id is ",extract_email_addresses(resume_txt) )


 Code to Read skills from any file 
skills = open("skillDB.txt", "r")
skills = skills.read()
print(skills)
listOfSkills = skills.split(",")
print(listOfSkills)

"""
