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
from nltk.corpus import wordnet, stopwords
from text_process import remove_stopwords, to_lowercase
import os
cachedStopWords = stopwords.words("english")

global programming_skill
programming_skill = ['devops','assembly','bash','c++','c#','coffeescript','emacs lisp','go!','groov','askell','java','javascript','matlab','max msp','objective c','perl','php','html','xml','css','processing','python','ruby','sml','swift','sic','wolfram language','xquery','sql','node.js','scala','kdb','jquery','mongodb','cmmi','iso','mysql','ms access','banking & finance--master','banking & finance--master','banking & finance-master','banking & finance-master','general ledge','finacle','oracle flexcube','fiserv','tcs bancs','fis profile','agile','c++-microsoft technologies--expert','scala','asp.net--master','dot net','ajax',' jquery','angular js 2.0','javascript','mvc','silverlight','jquery','asp.net','sql server 2005','java','liferay','jboss esb','eclipse','spring','hibernate','j2ee','core java','junit','log4j','version control','restful','rest','jsp','ms sharepoint cloud',' sharepoint','share point 2007','isms','selenium','codedui','coded-ui','automation','vb.net','vb','linux','ubuntu','wcag 2.0','seo','google analytics ','troubleshooting','analytics','wordpress','html','javascript','jquery','dom','php','mysql','stored procedures','apache','nginx','phpstorm','visual studio code','eclipse','git','jira','openshift','linux command line','b.tech','sap','mba','oracle','is oil','tsw','hydrocarbon product management','transportation management','sales and distribution','sap sd','sap mm','sap fi','AL/ML','AI','ML','artificial intelligence','machine learning','data science']
global keywords_list
keywords_list = ['consulting services','analyzing data','public policy','cross-functional team','DNS','risk assessment','machine learning','circuits','consulting experience','real-time','HTML5','iOS','annual budget','small business','cost reduction','IT infrastructure','litigation','business continuity','manage projects','computer software','affiliate','SQL server','physical security','internal audit','raw materials','sales operations','risk assessments','computer applications','operations management','software development life cycle','revenue growth','travel','international','web services','process development','customer facing','information system','CPG','experimental','GAAP','Flex','RFPs','Unix','budget management','SCI','LAN','prototype','SolidWorks','alliances','datasets','statistical analysis','help desk','VMware','journal entries','big data','co-op','CFA','office software','strategic initiatives','data quality','research projects','business issues','telecom','internal controls','test cases','APIs','quality management','benchmark','PeopleSoft','driving record','field sales','ETL','product design','immigration','daily operations','OS','media relations','spelling','retention','standardization','MS Project','Tableau','general ledger','therapeutic','MIS','software engineering','migration','scripting','deposits','chemicals','sales goals','mining','CPR','underwriting','strong analytical skills','beverage','product quality','financial reports','IBM','client services','internal communications','photography','talent acquisition','GIS','contract management','segmentation','hotels','trade shows','vendor management','root cause','strategic plans','cash flow','event planning','program development','Twitter','Adobe Creative Suite','API','sales management','cost effective','employee engagement','MATLAB','data center','in-store','instructional design','German','HRIS','public health','accounts receivable','business systems','project planning','front-end','matrix','startup','.NET','information management','transport','graphic design','management consulting','performance improvement','InDesign','outsourcing','lighting','performance metrics','inventory management','counsel','medical device','internal customers','travel arrangements','financing','UI','variances','test plans','FDA','MS Excel','project plan','commissioning','pharmacy','usability','supervisory experience','admissions','technical issues','business stakeholders','product knowledge','phone calls','JIRA','drafting','product line','status reports','KPI','AWS','regulatory compliance','quality standards','on-boarding','SDLC','relationship building','leadership development','analysis','root cause','business planning','end user','development activities','mortgage','physics','resource management','marketing materials','psychology','customer requirements','financial performance','UX','fabrication','portfolio management','broadcast','RFP','industry trends','value proposition','case management','fitness','Microsoft Office Suite','financial statements','analyze data','CMS','tablets','stakeholder management','talent management','on-call','technical knowledge','C#','standard operating procedures','operational excellence','SEO','project delivery','financial reporting','prospecting','digital media','SAS','SOPs','intranet','EMEA','Microsoft Word','asset management','external partners','dynamic environment','reconcile','architectures','algorithms','iPhone','business management','due diligence','marketing plans','non-profit','routing','workflows','electrical engineering','start-up','biology','operating systems','marketing strategy','support services','invoicing','build relationships','business cases','human resource','technical skills','experiments','call center','law enforcement','strategic direction','instrumentation','TV','acquisitions','purchase orders','AutoCAD','industry experience','accounts payable','Python','supply chain management','aviation','information security','ITIL','regulatory requirements','product marketing','internal stakeholders','Cisco','analytical skills','cloud','client relationships','user experience','business plans','financial management','marketing programs','higher education','data collection','D (programming language)','journalism','e-commerce','sports','Photoshop','scrum','key performance indicators','complex projects','supervising','publishing','client service','C++','business intelligence','ecommerce','financial analysis','business analysis','conversion','CSS','reconciliation','quality control','data management','PMP','business strategy','warehouse','market research','ISO','repairs','fundraising','Adobe','licensing','security clearance','android','employee relations','auditing','mechanical engineering','hospitality','six sigma','project management skills','audio','customer-facing','mathematics','sales experience','CAD','SaaS','chemistry','process improvements','researching','relationship management','real estate','life cycle','branding','ordering','hotel','data entry','SharePoint','proposal','recruit','spreadsheets','Facebook','Linux','digital marketing','assembly','Javascript','public relations','PR','electronics','valid drivers license','business process','account management','editorial','investigate','service delivery','tax','positioning','fulfillment','ERP','pharmaceutical','teaching','Java','oracle','software development','QA','internship','publications','HTML','fashion','BI','performance management','frameworks','technical support','counseling','MS Office','strategic planning','legislation','financial services','consumers','business administration','nursing','information systems','documenting','Salesforce','drawings','business requirements','Merchandising','Microsoft Office','sourcing','outreach','banking','windows','quality assurance','program management','protocols','coding','statistics','data analysis','R (programming language)','payroll','investigations','transactions','risk management','installation','process improvement','lean','payments','administrative support','invoices','video','change management','billing','expenses','acquisition','forecasts','hospital','KPIs','purchasing','editing','SQL','investigation','modeling','filing','lifecycle','automation','social media','transportation','information technology','economics','I-DEAS','customer experience','electrical','budgeting','computer science','troubleshooting','SAP','CRM','product management','recruiting','networking','product development','continuous improvement','staffing','governance','supply chain','architecture','audit','business development','advertising','forecasting','agile','programming','hardware','negotiation','management experience','partnerships','partnership','procurement','recruitment','specifications','human resources','controls','Correspondence','C (programming language)','mobile','logistics','construction','scheduling','regulatory','healthcare','retail','inventory','contracts','writing','consulting','vendors','testing','coaching','distribution','analytics','database','engagement','legal','metrics','regulations','accounting','certification','safety','presentations','brand','presentation','content','documentation','customer service','health','project management','finance','budget','policies','engineering','analytical','research','strategy','compliance','reporting','marketing','sales','training','technical','operations','Design']
global soft_skills
soft_skills = ['team player','self-directed learning','collaboration','communication','resilience','big-picture mindset','prioritization ','creativity ','creative','insight','curiosity','curious','openness','teamwork','time management','emotional intelligence','quick learner','problem solver','customer-service skills','planning and organizing','innovative','thinking innovatively and creatively','resourceful','flexible','able to manage own time','having self-esteem','innovation skills','enterprise skills','civic or citizenship knowledge and skills','sociability','self-management','integrity','honesty','human resources','participates as a team member','works with diversity','exercises leadership','leadership','exercises leadership','monitors and corrects performance','understands systems','customer service','interpersonal skills','addressed','advertised','arbitrated','arranged','articulated','authored','clarified','collaborated','communicated','composed','condensed','conferred','consulted','contacted','conveyed','convinced','corresponded','debated','defined','developed','directed','discussed','drafted','edited','elicited','enlisted','explained','expressed','formulated','furnished','incorporated','influenced','interacted','interpreted','interviewed','involved','joined','judged','lectured','listened','marketed','mediated','moderated','negotiated','observed','outlined','participated','persuaded','presented','promoted','proposed','publicized','reconciled','recruited','referred','reinforced','reported','resolved','responded','solicited','specified','spoke','suggested','summarized','synthesized','translated','wrote','administered','analyzed','appointed','approved','assigned','attained','authorized','chaired','considered','consolidated','contracted','controlled','converted','coordinated','decided','delegated','developed','directed','eliminated','emphasized','enforced','enhanced','established','executed','generated','handled','headed','hired','hosted','improved','incorporated','increased','initiated','inspected','instituted','led','managed','merged','motivated','navigated','organized','originated','overhauled','oversaw','planned','presided','prioritized','produced','recommended','reorganized','replaced','restored','reviewed','scheduled','secured','selected','streamlined','strengthened','supervised','terminated','acted','adapted','began','combined','composed','conceptualized','condensed','created','customized','designed','developed','directed','displayed','drew','entertained','established','fashioned','formulated','founded','illustrated','initiated','instituted','integrated','introduced','invented','modeled','modified','originated','performed','photographed','planned','revised','revitalized','shaped','solved','administered','adjusted','allocated','analyzed','appraised','assessed','audited','balanced','budgeted','calculated','computed','conserved','corrected','determined','developed','estimated','forecasted','managed','marketed','measured','netted','planned','prepared','programmed','projected','qualified','reconciled','reduced','researched','retrieved','adapted','advocated','aided','answered','arranged','assessed','assisted','clarified','coached','collaborated','contributed','cooperated','counseled','demonstrated','diagnosed','educated','encouraged','ensured','expedited','facilitated','familiarized','furthered','guided','helped','insured','intervened','motivated','prevented','provided','referred','rehabilitated','represented','resolved','simplified','supplied','supported','volunteered','approved','arranged','catalogued','categorized','charted','classified','coded','collected','compiled','corrected','corresponded','distributed','executed','filed','generated','incorporated','inspected','logged','maintained','monitored','obtained','operated','ordered','organized','prepared','processed','provided','purchased','recorded','registered','reserved','responded','reviewed','routed','scheduled','screened','submitted','supplied','standardized','systematized','updated','validated','verified','analyzed','clarified','collected','compared','conducted','critiqued','detected','determined','diagnosed','evaluated','examined','experimented','explored','extracted','formulated','gathered','inspected','interviewed','invented','investigated','located','measured','organized','researched','reviewed','searched','solved','summarized','surveyed','systematized','tested','adapted','advised','clarified','coached','communicated','conducted','coordinated','critiqued','developed','enabled','encouraged','evaluated','explained','facilitated','focused','guided','individualized','informed','instilled','instructed','motivated','persuaded','simulated','stimulated','taught','tested','trained','transmitted','tutored','adapted','applied','assembled','built','calculated','computed','conserved','constructed','converted','debugged','designed','determined','developed','engineered','fabricated','fortified','installed','maintained','operated','overhauled','printed','programmed','rectified','regulated','remodeled','repaired','replaced','restored','solved','specialized','standardized','studied','upgraded','utilized']


#from collections import Counter
#import en_core_web_sm

def isJobTitleAvailable(jobTitle, tttt):
    if (tttt.lower().find(jobTitle.lower()) != -1): 
        result = "True"
        return result
    else: 
        result = "False"
        return result
    
#Function to extract names from the string using spacy
def extract_name(resume):
   
   # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = en_core_web_sm.load()
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(resume)
    for ent in doc.ents:
        if(ent.label_ == 'PER'):
            break 
    return ent.text                  

#Function to extract Phone Numbers from string using regular expressions
def extract_phone_numbers(string):
    #r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    #phone_numbers = r.findall(string)
    r = re.compile(r'\+\d \d{3}-\d{3}-\d{4}|\d \d{3}-\d{3}-\d{4}|\d-\d{3}-\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\d{3} \d{3} \d{4}|\d{10}|\+\d{2} \d{10}|\+\d{2}\d{10}|\d{10}|\(\d{3}\) \d{4}-\d{4}|\+\d{3} \d{4}-\d{4}|\d{4}-\d{4}|\d{3}-\d{4}|\(\d{4}\) \d{3}-\d{3}|\(\d{5}\) \d{2}-\d{4}|\(\d{3}\) \d{3}-\d{3}-\d{4}|\d{2} \d{5}-\d{4}|\d{3} \d{3} \d{3}|9 \d{4} \d{4}|\d{2} \d{4} \d{4}|9\d{4} \d{4}|\(0\d{2}\) \d{4}-\d{4}|\(0\d{3}\) \d{3}-\d{4}|\d{4} \d{4}|\+52 \d{4} \d{4}|\+52 \(\d{2}\) \d{4}-\d{4}|\+52 \d \d{5} \d{4}|\(\d{2}\) \d{4}-\d{4}|\(\d{3}\) \d{3}-\d{2}-\d{2}|\+52 \(\d{3}\) \d{3}-\d{2}-\d{2}|\+52 \d{3} \d{3} \d{4}|\d{3} \d{2} \d{2}|\d{3} \d{3} \d{4}|1 \d{3} \d{3}-\d{4}|0\d{5} \d{6}|\+44 \d{4} \d{6}|0\d{3} \d{6}|\+380 \d{2} \d{3} \d{2} \d{2}|\+38 0\d{2} \d{7}|\+38 \(0\d{2}\) \d{7}|1\d{2} \d{4} \d{4}|09\d{2} \d{3} \d{3}|\+98 9\d{2} \d{3} \d{4}|01\d{1}-\d{3} \d{4}|01\d{1}-\d{7}|\+63 \(\d{3}\) \d{3} \d{4}|0 \(\d{3}\) \d{3} \d{4}|\+65-\d{4}-\d{4}|\+65 \d{4} \d{4}|\(09\d\) \d{6}|09\d \d{6}|\(02\) \d{4} \d{4}|02 \d{8}|0\d \d{3} \d{4}|\+49 \d{2} \d{6}|\+49 \d{4} \d{6}|0\d{4} \d{5}|0\d \d{2} \d{2} \d{2} \d{2}|\d{2} \d{2} \d{2} \d{2}|\d{2} \d{3} \d{3}|\d{8}|04\d{2} \d{2} \d{2} \d{2}|04\d{2} \d{3} \d{3}|08\d \d{3} \d{4}|01 \d{3} \d{4}|021 \d{3} \d{4}|064 \d{3} \d{4}|\d{3} \d{2} \d{3}|\(\d{3}\) \d{2} \d{3}|\(\d{2}\) \d{2} \d{2} \d{2}|\d{3} \d{2} \d{2} \d{2}')
    phone_numbers = r.findall(string)
    return phone_numbers

#Function to extract Email address from a string using regular expressions
def extract_email_addresses(string):
    string1 = string.replace(" @gmail", "@gmail") 
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string1.lower())

def extractPersonName(resumeText):
    resumeText = resumeText.lower()
    pattern = re.compile("\\b(resume|cv|curriculum vitae)\\W", re.I)
    resumeText =  pattern.sub("", resumeText)
    String = resumeText[:30]
    #String = re.split(r'\s{2,}', String)[0]
    String = String.split(' ')
    stopwords = ['mrs.','.','ms.','mr.','b','mr', 'ms', 'mrs', 'resume', 'cv', 'curriculum vitae']
    querywords = String.copy()
    resultwords  = [word for word in querywords if word.lower() not in stopwords]
    resultwords = resultwords[:5]
    result = ' '.join(resultwords)
    result = re.sub('[^A-Za-z0-9]+', ' ', result)
    result = ' '.join([word for word in result.split() if word not in cachedStopWords])
    result  = ' '.join([word for word in result.split() if word not in stopwords])
    result = ' '.join([word for word in result.split() if word not in programming_skill])
    result = ' '.join([word for word in result.split() if word not in keywords_list])
    result = ' '.join([word for word in result.split() if word not in soft_skills])
    
    namelist = re.split('; |, |\*|\n|email|phone|mobile|mob|e-mail',result)
    name = re.sub('[^A-Za-z0-9]+', ' ', namelist[0])
    name = name.lstrip()
    name = name.rstrip()
    
    Sentences = nltk.sent_tokenize(name)
    Tokens = []
    for Sent in Sentences:
        Tokens.append(nltk.word_tokenize(Sent)) 
    Words_List = [nltk.pos_tag(Token) for Token in Tokens]
    Nouns_List = []

    for List in Words_List:
        for Word in List:
            if re.match('[NN.*]|[JJ.*]|[CD.*]|[FW.*]', Word[1]):
                 Nouns_List.append(Word[0])

    NameList = Nouns_List[:2]
    Name = " ".join(NameList)
    return Name
     
    

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
