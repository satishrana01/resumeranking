import glob
import globals
import os
import warnings
from flask import (Flask,session,flash, redirect, render_template, request,
                   url_for, send_from_directory)
import core
import pandas as pd


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='admin',
    SECRET_KEY='development key',
))


app.config['UPLOAD_FOLDER'] = 'Upload-Resume'
app.config['UPLOAD_JD_FOLDER'] = 'Upload-JD'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'doc', 'docx'])

class jd:
    def __init__(self, df,resumeObject):
        self.df = df
        self.resumeObject = resumeObject

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/')
def home():
     
    return render_template('index.html')
@app.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        #os.chdir(app.config['UPLOAD_JD_FOLDER'])
        jd_file_path = globals.rootpath+globals.pathSeprator+app.config['UPLOAD_JD_FOLDER']+globals.pathSeprator
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


@app.route('/uploadResume', methods=['GET', 'POST'])
def uploadResume():
    return render_template('uploadresume.html')

@app.route("/upload", methods=['POST'])
def upload_file():
       
    resume_file_path = globals.rootpath+globals.pathSeprator+app.config['UPLOAD_FOLDER']+globals.pathSeprator
    if request.method=='POST' and 'customerfile' in request.files:
        for f in request.files.getlist('customerfile'):
            f.save(os.path.join(resume_file_path, f.filename))
            
        x = os.listdir(resume_file_path)
        return render_template("resultlist.html", name=x)
    
@app.route('/uploadjdDesc', methods=['GET', 'POST'])
def uploadjdDesc():
    return render_template('uploadjd.html')

@app.route("/uploadjd", methods=['POST'])
def upload_jd_file():
    
    jd_file_path = globals.rootpath+globals.pathSeprator+app.config['UPLOAD_JD_FOLDER']+globals.pathSeprator
    if request.method=='POST' and 'customerfile' in request.files:
               
        for f in request.files.getlist('customerfile'):
            f.save(os.path.join(jd_file_path, f.filename))
            
        x = os.listdir(jd_file_path)
        return render_template("resultlist.html", name=x)

@app.route('/Upload-Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Upload-Resume', filename)



if __name__ == '__main__':
   # app.run(debug = True) 
    # app.run('127.0.0.1' , 5000 , debug=True)
    globals.initialize()
    app.run('0.0.0.0' , 5000 , debug=True , threaded=True)
    
