from flask import Flask, render_template, request, redirect, url_for, session, g
import os

app = Flask(__name__)
app.secret_key = "123"
app.config['upload_folder'] = "static/files"

if not os.path.exists(app.config['upload_folder']):
    os.makedirs(app.config['upload_folder'])

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
    
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        course_name = request.form.get('course_name')
        contact = request.form.get('contact')
        mail_id = request.form.get('mail_id')
        upload_file(request)
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

users=[]
users.append(User(id=1, username= "jey", password="12345"))
users.append(User(id=2, username= "ram", password="56789"))
users.append(User(id=3, username= "kesavan", password="1996"))

@app.route("/student", methods=["POST", "GET"])

def student():
    if request.method=='POST':
        '''This is a logout button which is in content page, here i am redirecting a
        page without creating separate route for logout'''
        if 'logout' in request.form:
            #if 'userid' in session:
            session.pop('userid', None)
            return redirect(url_for('example'))
        

        uname=request.form['uname']
        upass=request.form['upass']
        
        for var in users:
            if var.username==uname and var.password==upass:
                session['userid']=var.id
                g.record=1
                return redirect(url_for('content'))
            else:
                g.record=0
        if g.record!=1:
            return redirect(url_for('student'))
        
        

    return render_template("student.html")


if __name__ == "__main__":
    app.run(debug=False, host='10000')
