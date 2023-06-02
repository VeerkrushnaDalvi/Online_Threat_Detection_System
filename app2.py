from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from chatbot import chatbot_response
import warnings
warnings.filterwarnings('ignore')
# from feature import FeatureExtraction

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///clientinfo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

# class to create the database
class Info(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(500),nullable=False)
    pasword=db.Column(db.String(20),nullable=False)

    # date_created=db.Column(db.DateTime,default=datetime.utcnow)

    # def __repr__(self)->str:
    #     return f'{self.sno} ------ {self.title}'

# @app.route('/') # to make multiple web pages
# @app.route('/',methods=['GET','POST'])
# def hello_world():
#     if request.method=='POST':
#         print('post')
#         title=request.form['title']
#         desc=request.form['desc']

#         todo=Info(title=title,desc=desc)

#         db.session.add(todo)
#         db.session.commit()

#     allTodo=Info.query.all()
#     return render_template("index.html",allTodo=allTodo)    # runs the webpage, putted in templates folder

def search(email,password):
    allinfo=Info.query.all()

    for i in allinfo:
        if i.email==email and i.pasword==password:
            print("Record found....")
            return True
    return False

@app.route('/')
def Homepage():
    return render_template('home.html')

@app.route('/abc')
def LogSign():
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        # print(request.form['email_L'],request.form['password_L'])
        email,password=request.form['email_L'],request.form['password_L']
        check=search(email,password)
        print(check)
        print(email,password)
        if check:
            return f"Hello {email} You have loged in successfully...."
        else:
            return "Record not found...."
    return render_template('index.html')

    # return "login page"
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name_R']
        email=request.form['email_R']
        password=request.form['password_R']
        # confpass=request.form['conformpass_R']
        print(name)
        print(email)
        print(password)
        # add the data to the database
        info=Info(name=name,email=email,pasword=password)
        db.session.add(info)
        db.session.commit()

        # check the details
        allinfo=Info.query.all()
        # print(list(allinfo))
        row1=allinfo[0]
        print(row1.name)
        print(row1.email)
        print(row1.pasword)
        return "registration successfully..."

    # allinfo=Info.query.all()
    # print(list(allinfo))
    return render_template('index.html')


@app.post('/predict')
def predict():
    text=request.get_json().get("message")
    response=chatbot_response(text)
    # jsonify message
    message={'answer':response}

    return jsonify(message)

# @app.route()
# def Spamemail():
#     return render_template('email.html')
if __name__=='__main__':
    app.run(debug=True)