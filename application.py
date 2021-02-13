import glob
import os
import time
import warnings
from flask import (Flask,session,flash, redirect, render_template, request,
                   url_for, send_from_directory,jsonify,g, abort,Response)
import core
from flask_bcrypt import Bcrypt
import pandas as pd
import nltk
import json
from extract_exp import ExtractExp
import jsoncore as jsoncore
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
import s3fs
from time import gmtime, strftime
from datetime import datetime
import shutil

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

application = Flask(__name__)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(application)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')
nltk.download('wordnet')
global rootpath
rootpath = os.getcwd()
global pathSeprator
pathSeprator = '/'
global bucket_name
bucket_name = 'resume-rank-bucket'
Ordered_list_jd = []
Jd_total_exp_vector = []

#application.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
application.config['UPLOAD_FOLDER'] = 'Upload-Resume'
application.config['UPLOAD_JD_FOLDER'] = 'Upload-JD'
application.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'doc', 'docx'])
application.config['SECRET_KEY'] = '93be4be0-af90-44f3-b505-a473e099fb0f'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(application)
auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            application.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, application.config['SECRET_KEY'],
                              algorithms=['HS256'])
							  
        except:
            return
        return User.query.get(data['id'])


@auth.verify_password
def verify_password(username_or_token, password='test'):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@application.route('/api/users', methods=['POST'])
def new_user():
    input_json = request.get_json()
    username = input_json["username"]
    password = input_json["password"]
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})

@application.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@application.route('/api/rank/token',methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@application.route('/login', methods=['GET', 'POST'])
def login():
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
    checkSession() 
    return render_template('index.html')

"""
@application.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        #os.chdir(app.config['UPLOAD_JD_FOLDER'])
        jd_file_path = rootpath+pathSeprator+application.config['UPLOAD_JD_FOLDER']+pathSeprator
        files = glob.glob(jd_file_path+'*.xlsx')
        result = []
        print("JD files to be processed ",len(files))
        for file in files:
            data_set = pd.read_excel(file)
            search_st = data_set['High Level Job Description'][0].lower()
            skill_text = data_set['Technology'][0] + data_set['Primary Skill'][0].lower()
            jd_exp = data_set['Yrs Of Exp '][0]
            title = data_set['Job Title'][0].lower()
            min_qual = data_set['Minimum Qualification'][0].lower()
            flask_return = core.res(search_st,skill_text,jd_exp,min_qual, title)
            df = pd.DataFrame(columns=['Title','Experience','Primary Skill','Technology','Min Qualification'])
            df = df.append({'Title': title,'Experience':jd_exp,'Primary Skill':data_set['Primary Skill'][0],'Technology':data_set['Technology'][0],'Min Qualification':data_set['Minimum Qualification'][0],'Job Description':data_set['High Level Job Description'][0]}, ignore_index=True)
            obj = jd(df,flask_return)
            result.append(obj)
            
        return render_template('result.html', results = result)
        """

""" this method will return json response of scan """

""" input json 

{
   "userInfo":{
      "companyName":"abc",
      "name":"username"
   },
   "jobDetails":{
      "scan":"scan1"
   },
   "weightage":{
      "jd":15,
      "skill":35,
      "soft_skill":5,
      "experience":{
         "required":false,
         "allocation":30
      },
      "minimum_qualification":15
   },
   "mustHave":[
      "Must Have 1",
      "Must Have 2",
      "Must Have 3",
      "Must Have 4",
      "Must Have 5"
   ]
} """

		
@application.route('/api/rank/scan', methods=['POST'])
@auth.login_required
def scan():
    extract_exp = ExtractExp()
    s3 = boto3.resource('s3')
    root_path='temp/'
    if request.method == 'POST':
        #os.chdir(app.config['UPLOAD_JD_FOLDER'])
        LIST_OF_FILES_TXT_JD = []
        LIST_OF_FILES_XLSX_JD = []
        LIST_OF_FILES_JD = []
        s3_resource = boto3.resource("s3")
        fs = s3fs.S3FileSystem(anon=False)
        now = datetime.now()
        input_json = request.get_json()
        print("input request",input_json)
        aws_path = input_json["userInfo"]["name"]+pathSeprator+input_json["jobDetails"]["scan"]
        jd_file_path = bucket_name+pathSeprator+aws_path+pathSeprator+application.config['UPLOAD_JD_FOLDER']
        must_have_skill = input_json["mustHave"]
        input_job_present = False
        finalResult = {}
        finalResult["userInfo"] = { "companyName":input_json["userInfo"]["companyName"], "name":input_json["userInfo"]["name"], "accountType":input_json["userInfo"]["accountType"], "dateOfScan":now.strftime("%d/%m/%Y %H:%M:%S")}
        
        try:
            jobDescription = input_json["jobDetails"]["highLevelJobDescription"]
            if jobDescription:
                input_job_present = True
        except:
            print("no input jd")
            
        if(input_job_present):
            search_st = input_json["jobDetails"]["highLevelJobDescription"].lower()
            skill_text = input_json["jobDetails"]["technology"].lower() + input_json["jobDetails"]["primarySkill"].lower()
            jd_exp = input_json["jobDetails"]["yrsOfExp"]
            title = input_json["jobDetails"]["jobTitle"].lower()
            min_qual = input_json["jobDetails"]["minimumQualification"].lower()
            flask_return = jsoncore.res(search_st,skill_text,jd_exp,min_qual, title,input_json,aws_path,must_have_skill, s3_resource, fs, bucket_name)
            finalResult[title]=flask_return
            final_json = json.dumps(finalResult,default=lambda o: o.__dict__)
            return Response(final_json,status=200,mimetype="application/json")
            
            
        
        for file in fs.glob(jd_file_path+'/*.xlsx'):
            LIST_OF_FILES_XLSX_JD.append(file)
        for file in fs.glob(jd_file_path+'/*.xls'):
            LIST_OF_FILES_XLSX_JD.append(file)    
        for file in fs.glob(jd_file_path+'/*.txt'):
            LIST_OF_FILES_TXT_JD.append(file)
            
        LIST_OF_FILES_JD = LIST_OF_FILES_TXT_JD + LIST_OF_FILES_XLSX_JD
        sub_dir = aws_path.split(pathSeprator)[0]
        final_path = root_path+sub_dir+strftime("%H%M%S", gmtime())
        if not os.path.exists(final_path):
            os.makedirs(final_path)
            print("directory created",final_path)
            
        for count,i in enumerate(LIST_OF_FILES_JD):
            i = i.replace(bucket_name+pathSeprator, "")
            head, fileName = os.path.split(i)
            path_to_read_file = final_path+pathSeprator+fileName
            s3.Bucket(bucket_name).download_file(i,path_to_read_file)
        
        for count,i in enumerate(LIST_OF_FILES_JD):
            Temp = i.rsplit('.',1)
            if Temp[-1] == "xlsx" or Temp[-1] == "xls":
                try:
                    print('JD file name {}'.format(i))
                    temp_path = i.rsplit('/',1)
                    data_set = pd.read_excel(final_path+pathSeprator+temp_path[1])
                    search_st = data_set['High Level Job Description'][0].lower()
                    skill_text = data_set['Technology'][0] + data_set['Primary Skill'][0].lower()
                    jd_exp = data_set['Yrs Of Exp '][0]
                    title = data_set['Job Title'][0].lower()
                    min_qual = data_set['Minimum Qualification'][0].lower()
                    flask_return = jsoncore.res(search_st,skill_text,jd_exp,min_qual, title,input_json,aws_path,must_have_skill, s3_resource, fs, bucket_name)
                    finalResult[title]=flask_return
                    final_json = json.dumps(finalResult,default=lambda o: o.__dict__)
                    try:
                        shutil.rmtree(final_path, ignore_errors=True)
                    except:
                        print("unable to delete directory ",final_path)
                            
                    return Response(final_json,status=200,mimetype="application/json")
                except Exception as e: 
                    print(e)
                    #print(traceback.format_exc())
       
            
                
            elif Temp[-1] == "txt":  
                print(count," This is txt" , i)
                jd_text_data = []
                try:
                    temp_path = i.rsplit('/',1)
                    f = open(final_path+pathSeprator+temp_path[1],'r')
                    lines = f.readlines()
                    a =  "\n".join(lines)
                    c = [str(a)]
                    jd_text_data.extend(c)
                    f.close()
                    search_st = jd_text_data[0]
                    experience = extract_exp.get_features(search_st)
                    jd_exp = experience
                    title = jd_text_data[0][0:20] # Getting substring with initial 20 chars
                    min_qual = ""
                    flask_return = jsoncore.res(search_st,"",jd_exp,min_qual, title,input_json,aws_path,must_have_skill, s3_resource, fs, bucket_name)
                    finalResult[title]=flask_return
                    final_json = json.dumps(finalResult,default=lambda o: o.__dict__)
                    try:
                        shutil.rmtree(final_path, ignore_errors=True)
                    except:
                        print("unable to delete directory ",final_path)

                    return Response(final_json,status=200,mimetype="application/json")
                except Exception as e: print(e)    
        #print(finalResult)
        #return json.dumps(finalResult, separators=(',', ':'))
        #return application.response_class(response=Serializer.serialize(result),status=200,mimetype='application/json')
         
        """files = glob.glob(jd_file_path+'*.xlsx')
        finalResult = {}
        print("JD files to be processed ",len(files))
        for file in files:
            data_set = pd.read_excel(file)
            search_st = data_set['High Level Job Description'][0].lower()
            skill_text = data_set['Technology'][0] + data_set['Primary Skill'][0].lower()
            jd_exp = data_set['Yrs Of Exp '][0]
            title = data_set['Job Title'][0].lower()
            min_qual = data_set['Minimum Qualification'][0].lower()
            flask_return = jsoncore.res(search_st,skill_text,jd_exp,min_qual, title,input_json,aws_path,must_have_skill)
            print(flask_return)
            finalResult[title]=flask_return
        
        #return jsonify(scanResult=finalResult)
        print(finalResult)
        return json.dumps(finalResult, separators=(',', ':'))
        #return application.response_class(response=Serializer.serialize(result),status=200,mimetype='application/json')'
"""
@application.route('/uploadResume', methods=['GET', 'POST'])
def uploadResume():
    checkSession()
    resume_file_path = rootpath+pathSeprator+application.config['UPLOAD_FOLDER']+pathSeprator
    x = os.listdir(resume_file_path)
    return render_template('uploadresume.html',name=x)

@application.route('/deleteResume/<file_name>', methods=['GET'])
def deleteResume(file_name):
    checkSession()
    file_path_to_delete = rootpath+pathSeprator+application.config['UPLOAD_FOLDER']+pathSeprator+file_name
    os.remove(file_path_to_delete)
    resume_file_path = rootpath+pathSeprator+application.config['UPLOAD_FOLDER']+pathSeprator
    x = os.listdir(resume_file_path)
    return render_template('uploadresume.html',name=x)

@application.route('/deleteAllResume', methods=['GET'])
def deleteAllResume():
    checkSession()
    file_path_to_delete = rootpath+pathSeprator+application.config['UPLOAD_FOLDER']+pathSeprator
    files = glob.glob(file_path_to_delete+'*')
    for f in files:
        os.remove(f)
    resume_file_path = rootpath+pathSeprator+application.config['UPLOAD_FOLDER']+pathSeprator
    x = os.listdir(resume_file_path)
    return render_template('uploadresume.html',name=x)

@application.route('/deleteJd/<file_name>', methods=['GET'])
def deleteJd(file_name):
    checkSession()
    file_path_to_delete = rootpath+pathSeprator+application.config['UPLOAD_JD_FOLDER']+pathSeprator+file_name
    os.remove(file_path_to_delete)
    jd_file_path = rootpath+pathSeprator+application.config['UPLOAD_JD_FOLDER']+pathSeprator
    x = os.listdir(jd_file_path)
    return render_template('uploadjd.html',name=x)

@application.route('/deleteAllJd', methods=['GET'])
def deleteAllJd():
    checkSession()
    file_path_to_delete = rootpath+pathSeprator+application.config['UPLOAD_JD_FOLDER']+pathSeprator
    files = glob.glob(file_path_to_delete+'*')
    for f in files:
        os.remove(f)
    jd_file_path = rootpath+pathSeprator+application.config['UPLOAD_JD_FOLDER']+pathSeprator
    x = os.listdir(jd_file_path)
    return render_template('uploadjd.html',name=x)

@application.route("/upload", methods=['POST'])
def upload_file():
    checkSession()   
    resume_file_path = rootpath+pathSeprator+application.config['UPLOAD_FOLDER']+pathSeprator
    if request.method=='POST' and 'customerfile' in request.files:
        for f in request.files.getlist('customerfile'):
            f.save(os.path.join(resume_file_path, f.filename))
            
        x = os.listdir(resume_file_path)
        return render_template("uploadresume.html", name=x)
    
@application.route('/uploadjdDesc', methods=['GET', 'POST'])
def uploadjdDesc():
    checkSession()
    jd_file_path = rootpath+pathSeprator+application.config['UPLOAD_JD_FOLDER']+pathSeprator
    x = os.listdir(jd_file_path)
    return render_template('uploadjd.html',name=x)

@application.route("/uploadjd", methods=['POST'])
def upload_jd_file():
    
    jd_file_path = rootpath+pathSeprator+application.config['UPLOAD_JD_FOLDER']+pathSeprator
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
    if isLoggedIn:
        return redirect(url_for('login'))

if __name__ == '__main__':
   # app.run(debug = True) 
    # app.run('127.0.0.1' , 5000 , debug=True)
    #initialize()
    if not os.path.exists('db.sqlite'):
        db.create_all()
    application.run(debug=True)
 