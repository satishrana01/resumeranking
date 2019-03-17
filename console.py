# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 23:16:58 2019

@author: satish.kumar
"""

import globals
import glob
import core
import pandas as pd
import time
import os

class ConsoleRunner:
    
    def __init__(self, df,jdName,resumeObject):
        self.df = df
        self.jdName = jdName
        self.resumeObject = resumeObject
    
      
    def main(self):
        jd_file_path = globals.rootpath+globals.pathSeprator+"Upload-JD"+globals.pathSeprator
        files = glob.glob(jd_file_path+'*.xlsx')
        result = []
        print("JD files to be processed ",len(files))
        for file in files:
            data_set = pd.read_excel(file)
            search_st = data_set['High Level Job Description'][0]
            skill_text = data_set['Technology'][0] + data_set['Primary Skill'][0]
            jd_exp = data_set['Yrs Of Exp '][0]
            title = data_set['Job Title'][0]
            flask_return = core.res(search_st,skill_text,jd_exp)
            df = pd.DataFrame(columns=['Title','Experience','Primary Skill','Technology'])
            df = df.append({'Title': title,'Experience':jd_exp,'Primary Skill':data_set['Primary Skill'][0],'Technology':data_set['Technology'][0],'Job Description':data_set['High Level Job Description'][0]}, ignore_index=True)
            obj = ConsoleRunner(df,os.path.basename(file),flask_return)
            result.append(obj)
                   
        self.exportOutput(result) 
        
    def exportOutput(self,result):
        output_path = globals.rootpath+globals.pathSeprator+"Output"+globals.pathSeprator+'output_'+str(time.strftime("%Y%m%d-%H%M%S"))+'.xlsx'
        writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
        for m in result:
            
            list_index = []
            list_ph = []
            list_email = []
            list_exp = []
            list_skill = []
            list_jd = []
            list_skill_w = []
            list_exp_w = []
            list_non_tech = []
            list_rating = []
            list_file = []
            count = 1
            
            for r in m.resumeObject:
                list_index.append(count)
                list_ph.append(r.phoneNo)
                list_email.append(r.email)
                list_exp.append(r.name)
                list_skill.append(r.skillList)
                list_jd.append(r.jd)
                list_skill_w.append(r.skillRank)
                list_exp_w.append(r.exp)
                list_non_tech.append(r.nonTechSkills)
                list_rating.append(r.finalRank)
                list_file.append(r.filename)
                count+=1
            df_result = pd.DataFrame({'S.No.':list_index,'PhoneNo':list_ph,'Email':list_email,
                                      'Experience':list_exp,'Skills':list_skill,'JD (15%)':list_jd,
                                      'skill (40%)':list_skill_w,'exp (40%)':list_exp_w,'Non_Tech Skills (5%)':list_non_tech,
                                      'Rating(%)':list_rating,'Resume':list_file,'JD-Name':m.jdName})
            #frames = [m.df,df_result]
            #result = pd.concat(frames)
            #m.df.to_excel(writer, sheet_name=str(m.df['Title'][0])[0:31:1])
            df_result.to_excel(writer, sheet_name=str(m.df['Title'][0])[0:31:1],index=False)
        
        writer.save()
        print('Output genrated at',output_path)


if __name__ == '__main__':
    runner = ConsoleRunner("Console Runner","","")
    globals.initialize()
    runner.main()
    