from flask import Flask, render_template
from flask_bootstrap import Bootstrap


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


@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/upload_page")
def upload_page():
    return render_template("upload_page.html")


@app.route("/upload", methods=["POST"])
def upload():
    pass


if __name__ == "__main__":
    PORT = 5000
    HOST = "0.0.0.0"
    DEBUG = True
    app.run(host=HOST, port=PORT, debug=DEBUG)
