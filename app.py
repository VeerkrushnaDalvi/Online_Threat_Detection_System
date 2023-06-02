from flask import Flask,redirect,url_for,render_template,request,jsonify
import numpy as np
import pandas as pd
# import os
from werkzeug.utils import secure_filename
from ProjFun import CheckNews,GetQR_URL
from flask_sqlalchemy import SQLAlchemy
from chatbot import chatbot_response
from sklearn import metrics
import warnings
import pickle
from FakeNews import CheckNews
import os
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("URL_PhisingMLP.pkl","rb")
file2 =open("Spam_DetectionNB.pkl", "rb")
# file3 =open("Spam_DetectionNB.pkl", "rb")
# file4 =open("Spam_DetectionNB.pkl", "rb")
mlp = pickle.load(file)
nb=pickle.load(file2)
file.close()

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=r'static/files'
app.config['LOGIN_STATUS']=False
app.config['USERNAME']=str('')
# app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///clientinfo.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

# db=SQLAlchemy(app)
# class Info(db.Model):
#     sno=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(150),nullable=False)
#     email=db.Column(db.String(500),nullable=False)
#     pasword=db.Column(db.String(20),nullable=False)


# def search(email,password):
#     allinfo=Info.query.all()

#     for i in allinfo:
#         if i.email==email and i.pasword==password:
#             print("Record found....")
#             return True
#     return False
# All Routings___________________________________

@app.route('/',methods=['GET','POST'])
def home():
    # if request.method=='POST':
    #     # Handle POST Request here
    #     return render_template('index.html')
    return render_template('index.html')




@app.route('/phishing_url')
def phishing_url():
    go_back='/'
    return render_template("phishing.html", go_back=go_back)


@app.route('/fake_news')
def fake_news():
    return render_template("fakenews.html")


@app.route('/spam_ham')
def spam_ham():
    return render_template("spam.html")

@app.route('/qr')
def qr():
    return render_template("qr.html")
# @app.route('/phishing_url')
# def phishing_url():
#     return render_template("phishing.html"])



# All Routings___________________________________


@app.route('/url_method', methods=['GET', 'POST'])
def url_method():
    if request.method == "POST":
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30)

        y_pred =mlp.predict(x)[0]
        #1 is safe
        #-1 is unsafe
        y_pro_phishing = mlp.predict_proba(x)[0,0]
        y_pro_non_phishing = mlp.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        go_back='/'
        return render_template('phishing.html',xx =round(y_pro_non_phishing,2),url=url, go_back=go_back)
    return render_template('phishing.html', xx=-1)

@app.route('/spam_method', methods=['GET', 'POST'])
def spam_method():
    # pass
    if request.method =="POST":
        l=[]
        msgbody=request.form["mailmsg"]
        print(msgbody)
        l.append(msgbody)
        print(l)
        SpamRes=nb.predict(l)
        SpamRes= SpamRes[0]
        SpamRes = int(SpamRes)
        # print(type(SpamRes))
        # if SpamRes==0:
        #     print("Email is safe")
        # else:
        #     print("Email is Spam")
    return render_template('spam.html', SpamRes=SpamRes)


@app.route('/fake_method', methods=['GET', 'POST'])
def fake_method():
    if request.method=='POST':
        news=request.form['news']
        print(news)
        ans=CheckNews(news)
    return render_template('fakenews.html',ans=ans,utxt=news)


@app.route('/qr_method', methods=['GET', 'POST'])
def qr_method():
    if request.method=='POST':
        # img=request.files['QRimg']
        # file_path=(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename))
        # img.save(file_path)
        status='This is : '
        img=request.files['QRimg']
        img.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename))
        print(file_path)
        print('File Saved successfully...')
        imgfilename=img.filename
        print(imgfilename)
        qrUrl=GetQR_URL(file_path)
        if qrUrl=='NoQRcode':
            flag=1
        elif 'http' not in qrUrl:
            flag=2
        else:
            flag=0
            s=CheckURL(qrUrl)
            if s==1:
                status+="Safe"
            else:
                status+="Unsafe"
        # status="This is some thing"
        return render_template('qr.html',flname=imgfilename,qrcodeURL=qrUrl,flag=flag,status=status)
    return render_template('qr.html')

@app.post('/predict')
def predict():
    text=request.get_json().get("message")
    response=chatbot_response(text)
    # jsonify message
    message={'answer':response}

    return jsonify(message)


def CheckURL(url):
    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1,30)

    y_pred =mlp.predict(x)[0]
    #1 is safe
    #-1 is unsafe
    y_pro_phishing = mlp.predict_proba(x)[0,0]
    y_pro_non_phishing = mlp.predict_proba(x)[0,1]
    # if(y_pred ==1 ):
    pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
    #go_back='/'
    return y_pred

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=3000,debug=True)