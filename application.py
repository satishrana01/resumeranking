import glob
import globals
import os
import warnings
from flask import (Flask,session,flash, redirect, render_template, request,
                   url_for, send_from_directory)
import core
import pandas as pd


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

application = Flask(__name__)

#application.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
application.config.update(dict(
    USERNAME='admin',
    PASSWORD='admin',
    SECRET_KEY='development key',
))


application.config['UPLOAD_FOLDER'] = 'Upload-Resume'
application.config['UPLOAD_JD_FOLDER'] = 'Upload-JD'
application.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'doc', 'docx'])

class jd:
    def __init__(self, df,resumeObject):
        self.df = df
        self.resumeObject = resumeObject

@application.route('/login', methods=['GET', 'POST'])
def login():
    globals.initialize()
    session['logged_in'] = False
    error = None
    if request.method == 'POST':
        if request.form['username'] != application.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != application.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@application.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You were logged out')
    return redirect(url_for('login'))


@application.route('/')
def home():
    globals.initialize()
    checkSession() 
    return render_template('index.html')
@application.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        #os.chdir(app.config['UPLOAD_JD_FOLDER'])
        jd_file_path = globals.rootpath+globals.pathSeprator+application.config['UPLOAD_JD_FOLDER']+globals.pathSeprator
        files = glob.glob(jd_file_path+'*.xlsx')
        result = []
        print("JD files to be processed ",len(files))
        for file in files:
            data_set = pd.read_excel(file)
            search_st = data_set['High Level Job Description'][0]
            skill_text = data_set['Technology'][0] + data_set['Primary Skill'][0]
            jd_exp = data_set['Yrs Of Exp '][0]
            title = data_set['Job Title'][0]
            min_qual = data_set['Minimum Qualification'][0]
            flask_return = core.res(search_st,skill_text,jd_exp,min_qual)
            df = pd.DataFrame(columns=['Title','Experience','Primary Skill','Technology','Min Qualification'])
            df = df.append({'Title': title,'Experience':jd_exp,'Primary Skill':data_set['Primary Skill'][0],'Technology':data_set['Technology'][0],'Min Qualification':data_set['Minimum Qualification'][0],'Job Description':data_set['High Level Job Description'][0]}, ignore_index=True)
            obj = jd(df,flask_return)
            result.append(obj)
            
        return render_template('result.html', results = result)


@application.route('/uploadResume', methods=['GET', 'POST'])
def uploadResume():
    checkSession()
    resume_file_path = globals.rootpath+globals.pathSeprator+application.config['UPLOAD_FOLDER']+globals.pathSeprator
    x = os.listdir(resume_file_path)
    return render_template('uploadresume.html',name=x)

@application.route("/upload", methods=['POST'])
def upload_file():
    checkSession()   
    resume_file_path = globals.rootpath+globals.pathSeprator+application.config['UPLOAD_FOLDER']+globals.pathSeprator
    if request.method=='POST' and 'customerfile' in request.files:
        for f in request.files.getlist('customerfile'):
            f.save(os.path.join(resume_file_path, f.filename))
            
        x = os.listdir(resume_file_path)
        return render_template("uploadresume.html", name=x)
    
@application.route('/uploadjdDesc', methods=['GET', 'POST'])
def uploadjdDesc():
    checkSession()
    jd_file_path = globals.rootpath+globals.pathSeprator+application.config['UPLOAD_JD_FOLDER']+globals.pathSeprator
    x = os.listdir(jd_file_path)
    return render_template('uploadjd.html',name=x)

@application.route("/uploadjd", methods=['POST'])
def upload_jd_file():
    
    jd_file_path = globals.rootpath+globals.pathSeprator+application.config['UPLOAD_JD_FOLDER']+globals.pathSeprator
    if request.method=='POST' and 'customerfile' in request.files:
               
        for f in request.files.getlist('customerfile'):
            f.save(os.path.join(jd_file_path, f.filename))
            
        x = os.listdir(jd_file_path)
        return render_template("uploadjd.html", name=x)

@application.route('/Upload-Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Upload-Resume', filename)

@application.route('/Upload-JD/<path:filename>')
def custom_static_jd(filename):
    return send_from_directory('./Upload-JD', filename)

def checkSession():
    isLoggedIn = bool(session.get('logged_in'))
    print(isLoggedIn)
    if isLoggedIn:
        return redirect(url_for('login'))
       
if __name__ == '__main__':
   # app.run(debug = True) 
    # app.run('127.0.0.1' , 5000 , debug=True)
    globals.initialize()
    application.run()
    #app.run('0.0.0.0' , 5000 , debug=True , threaded=True)
    
