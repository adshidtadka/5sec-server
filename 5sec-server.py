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
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('models/schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()


@app.route('/result', methods=["POST"])
@cross_origin()
def result():
    user_name = request.form["userName"]
    result = request.form["result"]
    print(user_name)
    g.db.execute("INSERT INTO results(game_id, user_name, score) values (?, ?, ?)", [1, user_name, result])
    g.db.commit()
    return result


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response


if __name__ == '__main__':
    init_db()
    app.run()
