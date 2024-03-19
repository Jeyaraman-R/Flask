from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_mail import Mail, Message
import psycopg2 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy import text
#from sqlalchemy import create_engine
#from flask_mysqldb import MySQL
#from database.config import config
import os
app = Flask(__name__)
app.secret_key = "123"
#File Upload
app.config['upload_folder'] = "static/files"
#app.config.from_object(config)
#mysql=MySQL(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://root:PYohqeXEmcz8aLiJINZ7VGVbjbCgDcCe@dpg-cnrv0pol5elc73b39vgg-a.oregon-postgres.render.com/ram_mqj4'
db=SQLAlchemy(app)
#engine=create_engine('postgresql://root:PYohqeXEmcz8aLiJINZ7VGVbjbCgDcCe@dpg-cnrv0pol5elc73b39vgg-a.oregon-postgres.render.com/ram_mqj4')
if not os.path.exists(app.config['upload_folder']):
    os.makedirs(app.config['upload_folder'])

#DB configuration
'''app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="SYSTEM"
app.config['MYSQL_DB']="ram"
app.config['MYSQL_CURSORCLASS']="DictCursor"
mysql=MySQL(app)'''
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/example')
def example():
    return render_template("example.html")


@app.route('/source')
def source():
    name = "jey"
    return render_template("source.html", username=name)

@app.route('/process')
def process():
    return render_template("process.html")

@app.route('/application', methods=["POST", "GET"])
def application():
    def mail_con(mail_id):
        print("Mail function called with recipient:", mail_id) 
        try:            
            message="Submission Received"
            body='''Thank you for reaching out to us! We have received your response regarding application submisson. We appreciate you taking the time to contact us.

Our team is currently reviewing your message and will get back to you as soon as possible. Please rest assured that your inquiry is important to us, and we will do our best to address it promptly.

If you have any additional information or questions in the meantime, feel free to reply to this email, and we'll be happy to assist you further.

Once again, thank you for contacting us. We look forward to resolving your inquiry to your satisfaction.

Best regards,
Team Osai'''
            msg=Message(message, sender='ramfreelancer2021@gmail.com', recipients=[mail_id])
            msg.body=body
            mail.send(msg)
            print("Email sent successfully to:", mail_id) 
        except Exception as e:
            print("Error sending email:", str(e))

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        course_name = request.form.get('course_name')
        mail_id = request.form.get('mail_id')
        contact = request.form.get('contact')
        upload_file(request)
        #Email Configuration
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT']= 465
        app.config['MAIL_USE_TLS']= False
        app.config['MAIL_USE_SSL']= True
        app.config['MAIL_USERNAME']='ramfreelancer2021@gmail.com'
        app.config['MAIL_PASSWORD']='alqtaryjfwsdtcfq' 
        app.config['MAIL_DEFAULT_SENDER'] = ('Osai InfoTech', 'ramfreelancer2021@gmail.com')

        mail=Mail(app)
        #send_email = request.form.get('send_email')  
        if 'send_email' in request.form:  # If the checkbox is checked
            print("Checkbox is checked. Calling mail_con function.") 
            mail_con(mail_id)
            return render_template("result.html", name=name, age=age, course_name=course_name, contact=contact, mail_id=mail_id)    
            
        else:
            print("Checkbox is not checked. Not calling mail_con function.")
            return render_template("result.html", name=name, age=age, course_name=course_name, contact=contact, mail_id=mail_id)    
    else:
        return render_template("application.html")

def upload_file(request):
    upload_pdf = request.files['upload_pdf']
    if upload_pdf.filename != '':
        filepath = os.path.join(app.config["upload_folder"], upload_pdf.filename)
        upload_pdf.save(filepath)

@app.route("/content")
def content():
    return render_template("content.html")

class User():

    def __init__(self, id, username, password):
        self.id= id
        self.username= username
        self.password= password

'''users=[]
users.append(User(id=1, username= "jey", password="12345"))
users.append(User(id=2, username= "ram", password="56789"))
users.append(User(id=3, username= "kesavan", password="1996"))'''


@app.route('/register', methods=["GET", "POST"])
def register():
    try:
        if request.method=='POST':
            uname=request.form['uname']
            upass=request.form['upass']
            cpass=request.form['ucpass']
            if upass==cpass:
                #cur1=db.connect()
                db.session.begin()
                db.session.execute(text("insert into users(usname, pass) values (:uname,:upass)"),{"uname":uname,"upass":upass})
                # Commit changes to the database
                db.session.commit()
                
                # Close the cursor
                #cur1.close()
                db.session.close()
                return redirect(url_for('index'))
    except Exception as d:
        print(d)
        db.session.rollback()
    return render_template('register.html')

@app.route("/student", methods=["POST", "GET"])

def student():
    if request.method=='POST':
        '''This is a logout button which is in content page, here i am redirecting a
        page without creating separate route for logout'''
        if 'logout' in request.form:
            #if 'id' in session:
            session.pop('id', None)
            return redirect(url_for('index'))
        
        #From Html
        uname=request.form['uname']
        upass=request.form['upass']
        #From DB
        try:
            db.session.begin()
            data=db.session.execute(text("select * from users where usname=:uname AND pass=:upass"), {"uname":uname, "upass":upass})
            users=data.fetchone()
            if users:
                user_id = users[0] 
                session["id"]=user_id
                g.record=1
                return redirect(url_for('content'), code=302)
            else:
                g.record=0
            if g.record!=1:
                return redirect(url_for('student'))
        except Exception as d:
            print(d)
        finally:
            db.session.commit()
            #cur.close()
            db.session.close()
                      
    return render_template("student.html")
    
'''
        for var in users:
            if var.username==uname and var.password==upass:
                session['userid']=var.id
                g.record=1
                return redirect(url_for('content'), code=302)
            else:
                g.record=0
        if g.record!=1:
            return redirect(url_for('student'))'''
        
        
@app.route("/adcon")
def adcon():
    return render_template("adcon.html")
    

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method=='POST':
        '''This is a logout button which is in content page, here i am redirecting a
        page without creating separate route for logout'''
        if 'logout' in request.form:
            #if 'id' in session:
            session.pop('aid', None)
            return redirect(url_for('admin'))
        
        #From Html
        aname=request.form.get('aname')
        apass=request.form.get('apass')
        #From DB
        try:
            #cur=db.session()
            #cur5=engine.connect()
            #cur6=cur5.begin()
            db.session.begin()
            data1=db.session.execute(text("select * from admin where uname=:aname and upass=:apass"),{"aname":aname, "apass":apass})
            ausers=data1.fetchone()
            if ausers:
                ausers_id=ausers[0]
                session["aid"]=ausers_id
                g.record=1
                return redirect(url_for('adcon'), code=302)
            else:
                g.record=0
            if g.record!=1:
                return redirect(url_for('admin'))
        except Exception as d:
            print(d)
        finally:
            db.session.commit()
            #cur.close()
            db.session.close()
    return render_template("admin.html")

'''if __name__ == "__main__":
    app.run(debug=True)'''
