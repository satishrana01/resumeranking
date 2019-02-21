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
 