from types import MethodDescriptorType
from flask import Flask, render_template, redirect, request
import speech_recognition as sr
import smtplib
from email.message import EmailMessage


app = Flask(__name__)


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    # atext- audio text, *transcript of an audio file
    atext = ''
    
    if request.method == 'POST':
        
        if 'file-1' not in request.files:
            return redirect(request.url)
        else:
            # afile- audio file
            afile = request.files['file-1']
        
        if afile.filename == '':
            return redirect(request.url)
        elif afile:
            try:
                r = sr.Recognizer()

                with sr.AudioFile(afile) as source:
                    adata = r.record(source)
                atext = r.recognize_google(adata)
            
            except ValueError:
                return redirect(request.url)

    return render_template('index.html', transcript=atext)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print('rererere')
    return render_template('contact.html', title='Contanct')


@app.route('/form', methods=['POST'])
def form():  
    email = request.form.get('email')
    message = request.form.get('message')
        
    msg = EmailMessage()
    msg['Subject'] = 'dummy e-mail subject string'
    msg['From'] = 'my-email@gmail.com'
    msg['To'] = email
    msg.set_content('dummy e-mail content string')
    
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        # ecnryption
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        
        # use environment variables to store your e-mail password for .login
        smtp.login("my-email@gmail.com", "my-password")
        
        smtp.sendmail(msg)

      
    return render_template('form.html', email, message)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
