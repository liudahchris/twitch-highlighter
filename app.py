from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_bootstrap import Bootstrap
import os
from werkzeug.utils import secure_filename
from make_plots import make_plot


def create_app():
    '''
    Make a Flask-Bootstrap app
    Parameters:
        None
    Returns:
        Flask app
    '''
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()
UPLOAD_FOLDER = 'temp/'
ALLOWED_EXTENSIONS = set(['txt'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


@app.route("/")
def welcome():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    filename = "temp/{}".format(filename)
    make_plot(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               'temp.html')


if __name__ == "__main__":
    PORT = 5000
    HOST = "0.0.0.0"
    DEBUG = True
    app.run(host=HOST, port=PORT, debug=DEBUG)
