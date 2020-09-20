import os
import nltk

def initialize():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
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

 