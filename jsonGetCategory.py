import string
import os
from textblob import TextBlob
import collections
import nltk
nltk.download('punkt')

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

#Function defined for keyword matching for JD and Resume
def JDkeywordMatch(JDText, ResumeText, Weightage):
    keywords_list = ['consulting services','analyzing data','public policy','cross-functional team','DNS','risk assessment','machine learning','circuits','consulting experience','real-time','HTML5','iOS','annual budget','small business','cost reduction','IT infrastructure','litigation','business continuity','manage projects','computer software','affiliate','SQL server','physical security','internal audit','raw materials','sales operations','risk assessments','computer applications','operations management','software development life cycle','revenue growth','travel','international','web services','process development','customer facing','information system','CPG','experimental','GAAP','Flex','RFPs','Unix','budget management','SCI','LAN','prototype','SolidWorks','alliances','datasets','statistical analysis','help desk','VMware','journal entries','big data','co-op','CFA','office software','strategic initiatives','data quality','research projects','business issues','telecom','internal controls','test cases','APIs','quality management','benchmark','PeopleSoft','driving record','field sales','ETL','product design','immigration','daily operations','OS','media relations','spelling','retention','standardization','MS Project','Tableau','general ledger','therapeutic','MIS','software engineering','migration','scripting','deposits','chemicals','sales goals','mining','CPR','underwriting','strong analytical skills','beverage','product quality','financial reports','IBM','client services','internal communications','photography','talent acquisition','GIS','contract management','segmentation','hotels','trade shows','vendor management','root cause','strategic plans','cash flow','event planning','program development','Twitter','Adobe Creative Suite','API','sales management','cost effective','employee engagement','MATLAB','data center','in-store','instructional design','German','HRIS','public health','accounts receivable','business systems','project planning','front-end','matrix','startup','.NET','information management','transport','graphic design','management consulting','performance improvement','InDesign','outsourcing','lighting','performance metrics','inventory management','counsel','medical device','internal customers','travel arrangements','financing','UI','variances','test plans','FDA','MS Excel','project plan','commissioning','pharmacy','usability','supervisory experience','admissions','technical issues','business stakeholders','product knowledge','phone calls','JIRA','drafting','product line','status reports','KPI','AWS','regulatory compliance','quality standards','on-boarding','SDLC','relationship building','leadership development','analysis','root cause','business planning','end user','development activities','mortgage','physics','resource management','marketing materials','psychology','customer requirements','financial performance','UX','fabrication','portfolio management','broadcast','RFP','industry trends','value proposition','case management','fitness','Microsoft Office Suite','financial statements','analyze data','CMS','tablets','stakeholder management','talent management','on-call','technical knowledge','C#','standard operating procedures','operational excellence','SEO','project delivery','financial reporting','prospecting','digital media','SAS','SOPs','intranet','EMEA','Microsoft Word','asset management','external partners','dynamic environment','reconcile','architectures','algorithms','iPhone','business management','due diligence','marketing plans','non-profit','routing','workflows','electrical engineering','start-up','biology','operating systems','marketing strategy','support services','invoicing','build relationships','business cases','human resource','technical skills','experiments','call center','law enforcement','strategic direction','instrumentation','TV','acquisitions','purchase orders','AutoCAD','industry experience','accounts payable','Python','supply chain management','aviation','information security','ITIL','regulatory requirements','product marketing','internal stakeholders','Cisco','analytical skills','cloud','client relationships','user experience','business plans','financial management','marketing programs','higher education','data collection','D (programming language)','journalism','e-commerce','sports','Photoshop','scrum','key performance indicators','complex projects','supervising','publishing','client service','C++','business intelligence','ecommerce','financial analysis','business analysis','conversion','CSS','reconciliation','quality control','data management','PMP','business strategy','warehouse','market research','ISO','repairs','fundraising','Adobe','licensing','security clearance','android','employee relations','auditing','mechanical engineering','hospitality','six sigma','project management skills','audio','customer-facing','mathematics','sales experience','CAD','SaaS','chemistry','process improvements','researching','relationship management','real estate','life cycle','branding','ordering','hotel','data entry','SharePoint','proposal','recruit','spreadsheets','Facebook','Linux','digital marketing','assembly','Javascript','public relations','PR','electronics','valid drivers license','business process','account management','editorial','investigate','service delivery','tax','positioning','fulfillment','ERP','pharmaceutical','teaching','Java','oracle','software development','QA','internship','publications','HTML','fashion','BI','performance management','frameworks','technical support','counseling','MS Office','strategic planning','legislation','financial services','consumers','business administration','nursing','information systems','documenting','Salesforce','drawings','business requirements','Merchandising','Microsoft Office','sourcing','outreach','banking','windows','quality assurance','program management','protocols','coding','statistics','data analysis','R (programming language)','payroll','investigations','transactions','risk management','installation','process improvement','lean','payments','administrative support','invoices','video','change management','billing','expenses','acquisition','forecasts','hospital','KPIs','purchasing','editing','SQL','investigation','modeling','filing','lifecycle','automation','social media','transportation','information technology','economics','I-DEAS','customer experience','electrical','budgeting','computer science','troubleshooting','SAP','CRM','product management','recruiting','networking','product development','continuous improvement','staffing','governance','supply chain','architecture','audit','business development','advertising','forecasting','agile','programming','hardware','negotiation','management experience','partnerships','partnership','procurement','recruitment','specifications','human resources','controls','Correspondence','C (programming language)','mobile','logistics','construction','scheduling','regulatory','healthcare','retail','inventory','contracts','writing','consulting','vendors','testing','coaching','distribution','analytics','database','engagement','legal','metrics','regulations','accounting','certification','safety','presentations','brand','presentation','content','documentation','customer service','health','project management','finance','budget','policies','engineering','analytical','research','strategy','compliance','reporting','marketing','sales','training','technical','operations','Design',
]
    
    JD_Keyword_Matched = []
    Resume_Keyword_Matched = []
    ResumJD_Missed = [] # keywords available in JD but not available in Resume
    ResumeJD_Matched = []
    jd_tokenised = nltk.word_tokenize(JDText)
    jd_WordList = [x.lower() for x in jd_tokenised]
    resume_tokenised =  nltk.word_tokenize(ResumeText)
    resume_WordList = [x.lower() for x in resume_tokenised]

    for keys in jd_WordList:
      if keys in keywords_list:
            JD_Keyword_Matched.append(keys)
    for keys in resume_WordList:
        if keys in keywords_list: 
            Resume_Keyword_Matched.append(keys)

    ResumJD_Missed = list(set(JD_Keyword_Matched)- set(Resume_Keyword_Matched))  

    for word in Resume_Keyword_Matched:
       if word in JD_Keyword_Matched:
           ResumeJD_Matched.append(word)

    print(JD_Keyword_Matched)
    print(Resume_Keyword_Matched)
    print("matches are ", ResumeJD_Matched)
    print("misses are ", ResumJD_Missed)
    finalResult = {}
    JD_freq = {} 
    Resume_freq = {}
    for item in JD_Keyword_Matched: 
        if (item in JD_freq): 
            JD_freq[item] += 1
        else: 
            JD_freq[item] = 1

    for item in Resume_Keyword_Matched: 
        if (item in Resume_freq): 
            Resume_freq[item] += 1
        else: 
            Resume_freq[item] = 1

    JD_freq = collections.OrderedDict(sorted(JD_freq.items()))   
    Resume_freq = collections.OrderedDict(sorted(Resume_freq.items()))

    print("JD Freq dict is ", JD_freq)
    print("Resume Freq Dict is ",Resume_freq)

    # Rank logic
    percent_EachJDKeywords = round(Weightage/len(JD_freq))
    print("percent assigned to each jd keyword is ", percent_EachJDKeywords)

    main_JD_keys = list(set(JD_Keyword_Matched))
    print("main keys found in JD are ", main_JD_keys)
    perc_Dict = dict((k,percent_EachJDKeywords) for k in main_JD_keys)
    print("Percentage distributed across all JD keywords are ",perc_Dict)

    # Ranking
    rank_dict = {}
    FinalPercentage = 0
    for key in main_JD_keys:
        if key in  Resume_Keyword_Matched:
          if (Resume_freq.get(key) >= JD_freq.get(key)):
            value = perc_Dict.get(key)
            rank_dict[key] = value
          else:
            value = (Resume_freq.get(key)/JD_freq.get(key))*perc_Dict.get(key)
            rank_dict[key] = value
        else:
            rank_dict[key] = 0

    print("Rank dict is ", rank_dict)

    for k,v in rank_dict.items():
       FinalPercentage = FinalPercentage + v

    print("Final percentage is ", FinalPercentage)
    finalResult['rank'] = FinalPercentage
    finalResult['jdKeywordMatch'] = JD_freq
    finalResult['jdKeywordUnMatched'] = ResumJD_Missed
    
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