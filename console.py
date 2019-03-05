# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 23:16:58 2019

@author: satish.kumar
"""

import globals
import glob
import core
import pandas as pd

class ConsoleRunner:
    
    def __init__(self, df,resumeObject):
        self.df = df
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
            obj = ConsoleRunner(df,flask_return)
            result.append(obj)
            print(result)


if __name__ == '__main__':
    runner = ConsoleRunner("Console Runner","")
    globals.initialize()
    runner.main()
    