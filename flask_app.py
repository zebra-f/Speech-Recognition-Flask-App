from flask import Flask, render_template, redirect, request
import speech_recognition as sr


app = Flask(__name__)


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    # atext- audio text, *transcript of an audio file
    atext = ''
    
    if request.method == 'POST':
        print('data recived')
        
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


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contanct')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)