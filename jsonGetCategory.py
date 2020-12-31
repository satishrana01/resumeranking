import string
import os
from textblob import TextBlob
import collections
import nltk

global rootpath
rootpath = os.getcwd()
global pathSeprator
pathSeprator = '/'
global skill_threshold
skill_threshold = 1

global programming_skill
programming_skill = ['devops','assembly','bash','c++','c#','coffeescript','emacs lisp','go!','groov','askell','java','javascript','matlab','max msp','objective c','perl','php','html','xml','css','processing','python','ruby','sml','swift','sic','wolfram language','xquery','sql','node.js','scala','kdb','jquery','mongodb','cmmi','iso','mysql','ms access','banking & finance--master','banking & finance--master','banking & finance-master','banking & finance-master','general ledge','finacle','oracle flexcube','fiserv','tcs bancs','fis profile','agile','c++-microsoft technologies--expert','scala','asp.net--master','dot net','ajax',' jquery','angular js 2.0','javascript','mvc','silverlight','jquery','asp.net','sql server 2005','java','liferay','jboss esb','eclipse','spring','hibernate','j2ee','core java','junit','log4j','version control','restfull','rest','jsp','ms sharepoint cloud',' sharepoint','share point 2007','isms','selenium','codedui','coded-ui','automation','vb.net','vb','linux','ubuntu','wcag 2.0','seo','google analytics ','troubleshooting','analytics','wordpress','html','javascript','jquery','dom','php','mysql','stored procedures','apache','nginx','phpstorm','visual studio code','eclipse','git','jira','openshift','linux command line','b.tech','sap','mba','oracle','is oil','tsw','hydrocarbon product management','transportation management','sales and distribution','sd','mm','fi']
global keywords_list
keywords_list = ['consulting services','analyzing data','public policy','cross-functional team','DNS','risk assessment','machine learning','circuits','consulting experience','real-time','HTML5','iOS','annual budget','small business','cost reduction','IT infrastructure','litigation','business continuity','manage projects','computer software','affiliate','SQL server','physical security','internal audit','raw materials','sales operations','risk assessments','computer applications','operations management','software development life cycle','revenue growth','travel','international','web services','process development','customer facing','information system','CPG','experimental','GAAP','Flex','RFPs','Unix','budget management','SCI','LAN','prototype','SolidWorks','alliances','datasets','statistical analysis','help desk','VMware','journal entries','big data','co-op','CFA','office software','strategic initiatives','data quality','research projects','business issues','telecom','internal controls','test cases','APIs','quality management','benchmark','PeopleSoft','driving record','field sales','ETL','product design','immigration','daily operations','OS','media relations','spelling','retention','standardization','MS Project','Tableau','general ledger','therapeutic','MIS','software engineering','migration','scripting','deposits','chemicals','sales goals','mining','CPR','underwriting','strong analytical skills','beverage','product quality','financial reports','IBM','client services','internal communications','photography','talent acquisition','GIS','contract management','segmentation','hotels','trade shows','vendor management','root cause','strategic plans','cash flow','event planning','program development','Twitter','Adobe Creative Suite','API','sales management','cost effective','employee engagement','MATLAB','data center','in-store','instructional design','German','HRIS','public health','accounts receivable','business systems','project planning','front-end','matrix','startup','.NET','information management','transport','graphic design','management consulting','performance improvement','InDesign','outsourcing','lighting','performance metrics','inventory management','counsel','medical device','internal customers','travel arrangements','financing','UI','variances','test plans','FDA','MS Excel','project plan','commissioning','pharmacy','usability','supervisory experience','admissions','technical issues','business stakeholders','product knowledge','phone calls','JIRA','drafting','product line','status reports','KPI','AWS','regulatory compliance','quality standards','on-boarding','SDLC','relationship building','leadership development','analysis','root cause','business planning','end user','development activities','mortgage','physics','resource management','marketing materials','psychology','customer requirements','financial performance','UX','fabrication','portfolio management','broadcast','RFP','industry trends','value proposition','case management','fitness','Microsoft Office Suite','financial statements','analyze data','CMS','tablets','stakeholder management','talent management','on-call','technical knowledge','C#','standard operating procedures','operational excellence','SEO','project delivery','financial reporting','prospecting','digital media','SAS','SOPs','intranet','EMEA','Microsoft Word','asset management','external partners','dynamic environment','reconcile','architectures','algorithms','iPhone','business management','due diligence','marketing plans','non-profit','routing','workflows','electrical engineering','start-up','biology','operating systems','marketing strategy','support services','invoicing','build relationships','business cases','human resource','technical skills','experiments','call center','law enforcement','strategic direction','instrumentation','TV','acquisitions','purchase orders','AutoCAD','industry experience','accounts payable','Python','supply chain management','aviation','information security','ITIL','regulatory requirements','product marketing','internal stakeholders','Cisco','analytical skills','cloud','client relationships','user experience','business plans','financial management','marketing programs','higher education','data collection','D (programming language)','journalism','e-commerce','sports','Photoshop','scrum','key performance indicators','complex projects','supervising','publishing','client service','C++','business intelligence','ecommerce','financial analysis','business analysis','conversion','CSS','reconciliation','quality control','data management','PMP','business strategy','warehouse','market research','ISO','repairs','fundraising','Adobe','licensing','security clearance','android','employee relations','auditing','mechanical engineering','hospitality','six sigma','project management skills','audio','customer-facing','mathematics','sales experience','CAD','SaaS','chemistry','process improvements','researching','relationship management','real estate','life cycle','branding','ordering','hotel','data entry','SharePoint','proposal','recruit','spreadsheets','Facebook','Linux','digital marketing','assembly','Javascript','public relations','PR','electronics','valid drivers license','business process','account management','editorial','investigate','service delivery','tax','positioning','fulfillment','ERP','pharmaceutical','teaching','Java','oracle','software development','QA','internship','publications','HTML','fashion','BI','performance management','frameworks','technical support','counseling','MS Office','strategic planning','legislation','financial services','consumers','business administration','nursing','information systems','documenting','Salesforce','drawings','business requirements','Merchandising','Microsoft Office','sourcing','outreach','banking','windows','quality assurance','program management','protocols','coding','statistics','data analysis','R (programming language)','payroll','investigations','transactions','risk management','installation','process improvement','lean','payments','administrative support','invoices','video','change management','billing','expenses','acquisition','forecasts','hospital','KPIs','purchasing','editing','SQL','investigation','modeling','filing','lifecycle','automation','social media','transportation','information technology','economics','I-DEAS','customer experience','electrical','budgeting','computer science','troubleshooting','SAP','CRM','product management','recruiting','networking','product development','continuous improvement','staffing','governance','supply chain','architecture','audit','business development','advertising','forecasting','agile','programming','hardware','negotiation','management experience','partnerships','partnership','procurement','recruitment','specifications','human resources','controls','Correspondence','C (programming language)','mobile','logistics','construction','scheduling','regulatory','healthcare','retail','inventory','contracts','writing','consulting','vendors','testing','coaching','distribution','analytics','database','engagement','legal','metrics','regulations','accounting','certification','safety','presentations','brand','presentation','content','documentation','customer service','health','project management','finance','budget','policies','engineering','analytical','research','strategy','compliance','reporting','marketing','sales','training','technical','operations','Design']
global soft_skills
soft_skills = ['team player','self-directed learning','collaboration','communication','resilience','big-picture mindset','prioritization ','creativity ','creative','insight','curiosity','curious','openness','teamwork','time management','emotional intelligence','quick learner','problem solver','customer-service skills','planning and organizing','innovative','thinking innovatively and creatively','resourceful','flexible','able to manage own time','having self-esteem','innovation skills','enterprise skills','civic or citizenship knowledge and skills','sociability','self-management','integrity','honesty','human resources','participates as a team member','works with diversity','exercises leadership','leadership','exercises leadership','monitors and corrects performance','understands systems','customer service','interpersonal skills','addressed','advertised','arbitrated','arranged','articulated','authored','clarified','collaborated','communicated','composed','condensed','conferred','consulted','contacted','conveyed','convinced','corresponded','debated','defined','developed','directed','discussed','drafted','edited','elicited','enlisted','explained','expressed','formulated','furnished','incorporated','influenced','interacted','interpreted','interviewed','involved','joined','judged','lectured','listened','marketed','mediated','moderated','negotiated','observed','outlined','participated','persuaded','presented','promoted','proposed','publicized','reconciled','recruited','referred','reinforced','reported','resolved','responded','solicited','specified','spoke','suggested','summarized','synthesized','translated','wrote','administered','analyzed','appointed','approved','assigned','attained','authorized','chaired','considered','consolidated','contracted','controlled','converted','coordinated','decided','delegated','developed','directed','eliminated','emphasized','enforced','enhanced','established','executed','generated','handled','headed','hired','hosted','improved','incorporated','increased','initiated','inspected','instituted','led','managed','merged','motivated','navigated','organized','originated','overhauled','oversaw','planned','presided','prioritized','produced','recommended','reorganized','replaced','restored','reviewed','scheduled','secured','selected','streamlined','strengthened','supervised','terminated','acted','adapted','began','combined','composed','conceptualized','condensed','created','customized','designed','developed','directed','displayed','drew','entertained','established','fashioned','formulated','founded','illustrated','initiated','instituted','integrated','introduced','invented','modeled','modified','originated','performed','photographed','planned','revised','revitalized','shaped','solved','administered','adjusted','allocated','analyzed','appraised','assessed','audited','balanced','budgeted','calculated','computed','conserved','corrected','determined','developed','estimated','forecasted','managed','marketed','measured','netted','planned','prepared','programmed','projected','qualified','reconciled','reduced','researched','retrieved','adapted','advocated','aided','answered','arranged','assessed','assisted','clarified','coached','collaborated','contributed','cooperated','counseled','demonstrated','diagnosed','educated','encouraged','ensured','expedited','facilitated','familiarized','furthered','guided','helped','insured','intervened','motivated','prevented','provided','referred','rehabilitated','represented','resolved','simplified','supplied','supported','volunteered','approved','arranged','catalogued','categorized','charted','classified','coded','collected','compiled','corrected','corresponded','distributed','executed','filed','generated','incorporated','inspected','logged','maintained','monitored','obtained','operated','ordered','organized','prepared','processed','provided','purchased','recorded','registered','reserved','responded','reviewed','routed','scheduled','screened','submitted','supplied','standardized','systematized','updated','validated','verified','analyzed','clarified','collected','compared','conducted','critiqued','detected','determined','diagnosed','evaluated','examined','experimented','explored','extracted','formulated','gathered','inspected','interviewed','invented','investigated','located','measured','organized','researched','reviewed','searched','solved','summarized','surveyed','systematized','tested','adapted','advised','clarified','coached','communicated','conducted','coordinated','critiqued','developed','enabled','encouraged','evaluated','explained','facilitated','focused','guided','individualized','informed','instilled','instructed','motivated','persuaded','simulated','stimulated','taught','tested','trained','transmitted','tutored','adapted','applied','assembled','built','calculated','computed','conserved','constructed','converted','debugged','designed','determined','developed','engineered','fabricated','fortified','installed','maintained','operated','overhauled','printed','programmed','rectified','regulated','remodeled','repaired','replaced','restored','solved','specialized','standardized','studied','upgraded','utilized']


def programmingScore(resume, jdTxt,skill_weightage):
    
    
    programmingTotal = 0
    jdSkillMatched = []
    for i in range(len(programming_skill)):
        if programming_skill[i] in jdTxt.lower() != -1:
            jdSkillMatched.append(programming_skill[i])
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

def minQualificationScore(resume, jdTxt,min_qual_weightage):
    programmingTotal = 0
    jdSkillMatched = []
    for i in range(len(programming_skill)):
        if programming_skill[i] in jdTxt.lower() != -1:
            #jdSkillCount += 1
            jdSkillMatched.append(programming_skill[i])
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
   
    jdSkillMatched = []
    skillMatched = []
    skillNotMatched = []
    finalResult ={}

    for i in range(len(programming_skill)):
        if programming_skill[i] in jdTxt.lower() != -1:
            jdSkillMatched.append(programming_skill[i])
        
    
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

    match_dictionary = {}
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
    
    ResumeJD_Matched = list(set(ResumeJD_Matched))
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
    
    # Get match dictionary
    match_dictionary = {key: value for key, value in Resume_freq.items() if key in ResumeJD_Matched}
    #print("match dictionary is ", match_dictionary)
    
    # Rank logic
    percent_EachJDKeywords = round(Weightage/len(JD_freq))
    main_JD_keys = list(set(JD_Keyword_Matched))
    perc_Dict = dict((k,percent_EachJDKeywords) for k in main_JD_keys)

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

    for k,v in rank_dict.items():
       FinalPercentage = FinalPercentage + v

    finalResult['rank'] = FinalPercentage
    finalResult['jdKeywordMatch'] = match_dictionary
    finalResult['jdKeywordUnMatched'] = ResumJD_Missed
    
    return finalResult   

def nonTechSkillSetListMatchedWithJD(resume, jdTxt,rank):
   
    jdSkillMatched = []
    skillMatched = []
    skillUnMatched = []
    finalResult = {}
    for i in range(len(soft_skills)):
        if soft_skills[i] in jdTxt.lower() != -1:
            jdSkillMatched.append(soft_skills[i])
    
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

@staticmethod
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


def NonTechnicalSkillScore(resume, jd_txt,non_tech_weightage):
    
    if non_tech_weightage == 0:
        non_tech_weightage = 1
        
    jdSkillMatched = []
    for i in range(len(soft_skills)):
        if soft_skills[i] in jd_txt.lower() != -1:
            jdSkillMatched.append(soft_skills[i])
    
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
    
    if(len(must_have_skill) == 0):
        return False
    
    for skill in must_have_skill:
        if skill.lower() in resumeText:
            return False
        
    return True    