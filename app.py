import os
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
FILE_DIR = 'files'

app = Flask(__name__)

if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = FILE_DIR + '/' + secure_filename(file.filename)
            file.save(filename)
            parsed = reader.readtext(filename)
            text = '<br/>\n'.join(map(lambda x: x[1], parsed))
            # handle file upload
            return (text)


    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=8080)
