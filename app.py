##CHB: you really don't want all this in one file
##     at least break out the models (DB stuff) from the views

from flask import Flask, render_template, request, redirect,url_for,session, abort

from flask_sqlalchemy import SQLAlchemy
    
import calendar


app = Flask(__name__)

#sqlalchemy configuration 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://abdishu:mypasswd@localhost/occflask'
# #instiatation data base 

db = SQLAlchemy(app)
# #Comment is table name 

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
##CHB: does SQLAlchemy suporrt an unlimited size text type??
    comment = db.Column(db.String(1000))

    def __init__(self, name, comment):
        self.name = name
        self.comment= comment

class Register(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(20))
# kinda short for an email address!
    password = db.Column(db.String(255))

    def __init__(self, name, email,password):
        self.name = name
        self.email= email
        self.password = password


class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(25))
    phone = db.Column(db.String(25))
 ## is there not a time Type?
    time = db.Column(db.String(25))
    budget = db.Column(db.String(25))
    donate = db.Column(db.String(25))
    services = db.Column(db.String(25))

    def __init__(self, name, email,phone,time,budget,donate,services):
        self.name = name
        self.email= email
        self.phone= phone
        self.time=time
        self.buget=budget
        self.donate=donate
        self.services= services


app.secret_key = "This is very secret"

@app.route('/')  
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    name = request.form.get("name") or None
    password = request.form.get("password") or None

    name = Register.query.filter_by(name=name)
    password = Register.query.filter_by(password=password)

    ## you don't want to store the password as plain text!
    ##  I"m not security expert, but I think you want to store a hash of the password
    ##   then you check a hash of what they pass in against the has stored
    ##     import hashlib ....

    if request.method =='POST':

        if request.form['password'] == password and request.form['username'] == name:
            return render_template('about.html')
        else:
            return render_template('about.html')  # still working on user validation with posgres
    return index()    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')  
def home():
    return render_template('home.html')  

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register')
def register():
    name = request.form.get("name") or None
    email = request.form.get("email") or None
    password = request.form.get("password") or None

    Credential = Register(name=name,email=email,password=password)
    db.session.add(Credential)
    db.session.commit()

    return render_template('register.html')



@app.route('/browse')
def browse():
    
    return render_template('browse.html')

@app.route('/comment')
def comment():
    result = Comment.query.all()

    return render_template('comment.html',result=result)

@app.route('/sign')
def sign():
    return render_template('sign.html') 

@app.route('/process', methods=['POST'])
def process():
    name = request.form.get("name") or None
    comment = request.form.get("comment") or None

   # Adding to the data base

    occomments = Comment(name=name,comment=comment)
    db.session.add(occomments)
    db.session.commit() 
 #this save the change

    return render_template('comment.html', name= name, comment=comment)
 
    #"Your name is:" + name2 + "Your comment is:" +  comment

#Please note of GET AND POST 

@app.route('/submit/form', methods=['POST'])
def user():

    name = request.form.get("name") or None
    email = request.form.get("email") or None
    phone = request.form.get("phone") or None
    time = request.form.get("time") or None
    budget = request.form.get("budget") or None
    services = request.form.get("services") or None

    occmember = Contact(name=name,email=email,phone=phone,time=time,budget=budget,services=services)
    db.session.add(occmember)
    db.session.commit()

    if not name or not email or not phone:
        return "Please enter your name email and phone number! <br> <a href='/contact'>Back to Contact Form</a>"
    
    return render_template('user.html',name=name,email=email,phone=phone,time=time,budget=budget,services=services)

@app.route('/_register/', methods = ['POST'])

def _register():

    #if user logged in already do not register again using session 

    if 'loggedin' in session:
        return redirect(url_for('index'))
        
    name = request.form.get('name') or None
    email= request.form.get('email') or None
    password = request.form.get('password') or None

    if not email or not name or not password:
        return "Please enter all requirement <a href='/_register'> Register</a>"
    #to use session you need secret key 
        
    session["name"] = name
    session["email"]= email
    session["password"] = password
    session["loggedin"] = True


    return redirect (url_for('index'))

if __name__=="__main__":

    app.run(debug=True) 


 
