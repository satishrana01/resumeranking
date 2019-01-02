""" Below code is to extract experince from CV Text and compare with expected 
    JD experience and return weightage 
"""

from word2number import w2n
import spacy
import string
nlp = spacy.load('en_core_web_sm')

def get_exp(JD_exp,CV_text):
    CV_text  = str.replace(CV_text, 'yrs', 'year')
    CV_text  = str.replace(CV_text, 'yr', 'year')
    doc = nlp(CV_text)
    year_string = ''
    first_string ='zero'
    # Print out named entities
    for ent in doc.ents:
        years_of_experience = ent.text
        if("year" in years_of_experience):
            print(ent.text, ent.label_)
            year_string = ent.text
            break
    token_string = nlp(year_string)
    
    #catch the token
    for token in token_string:
        first_string = str(token)
        break
    #print("This is the splited string: ",first_string)
    
    if(not first_string.isdigit()):
        string_text = str(first_string)
        try:
            x=w2n.word_to_num(string_text)
        except Exception:
            x=0
        return(get_year_wtg(JD_exp,int(x)))
        
    return(get_year_wtg(JD_exp,first_string))    


def get_year_wtg(JD_exp,ext_exp):
    print("The extracted exp is: ",ext_exp)
    print("JD Expected experince range is :",JD_exp[:])
    exp_weightage = 40
    
    if((int(JD_exp[0]) == int(ext_exp)) or (int(JD_exp[2]) == int(ext_exp))):
        exp_weightage
    elif((int(JD_exp[0]) - 1 == int(ext_exp)) or (int(JD_exp[2]) +1 == int(ext_exp))):
        exp_weightage-=10 
    elif(int(JD_exp[0]) -2 == int(ext_exp)) or (int(JD_exp[2]) +2 == int(ext_exp)):
        exp_weightage-=20
    elif(int(JD_exp[0]) -3 == int(ext_exp)) or (int(JD_exp[2]) +3 == int(ext_exp)):
       exp_weightage-=30
    else:
        exp_weightage = 0
    return exp_weightage


def get_total_exp(JD_exp,CV_text):
    CV_text  = str.replace(CV_text, 'yrs', 'year')
    CV_text  = str.replace(CV_text, 'yr', 'year')    
    doc = nlp(CV_text)
    year_string = ''
    first_string ='zero'
    # Print out named entities
    for ent in doc.ents:
        years_of_experience = ent.text
        if("year" in years_of_experience):
            print(ent.text, ent.label_)
            year_string = ent.text
            break
    token_string = nlp(year_string)
    
    #catch the token
    for token in token_string:
        first_string = str(token)
        break
    #print("This is the splited string: ",first_string)
    
    if(not first_string.isdigit()):
        string_text = str(first_string)
        try:
            x=w2n.word_to_num(string_text)
        except Exception:
            x=0
        return (int(x))
        
    return first_string 



