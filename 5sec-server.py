from flask import Flask, request, g
from flask_cors import CORS, cross_origin
from contextlib import closing
import configparser
import sqlite3

# configuration
config = configparser.ConfigParser()
config.read("config.ini")
SERVER_NAME = config["DEFAULT"]["server_name"]
DEBUG = False
DATABASE = "models/5sec-server.db"

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)


@app.route('/result', methods=["POST"])
@cross_origin()
def result():
    user_name = request.form["userName"]
    result = request.form["result"]
    return result


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('models/schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()


if __name__ == '__main__':
    init_db()
    app.run()
