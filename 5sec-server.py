from flask import Flask, request, g, redirect, url_for
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


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('models/schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()


@app.route('/result', methods=["POST"])
@cross_origin()
def create_result():
    user_name = request.form["userName"]
    score = request.form["score"]
    g.db.execute("INSERT INTO results(game_id, user_name, score) VALUES (?, ?, ?)", [1, user_name, score])
    g.db.commit()
    return redirect(url_for("get_result"))


@app.route('/result', methods=["GET"])
@cross_origin()
def get_result():
    results = g.db.execute("SELECT * FROM results ORDER BY score")
    results_list = [dict(id=row[0], game_id=row[1], user_name=row[2], score=row[3]) for row in results.fetchall()]
    return {"data": results_list}


@app.route("/game", methods=["GET"])
@cross_origin()
def get_game():
    game_tuple = g.db.execute("SELECT id, max(start_time), user_num FROM games WHERE start_time >= (SELECT DATETIME('NOW', 'LOCALTIME'))").fetchone()
    if game_tuple[0] == None:
        return redirect(url_for("create_game"))
    else:
        game_dict = dict(id=game_tuple[0], start_time=game_tuple[1], user_num=game_tuple[2])
        return {"data": game_dict}


@app.route("/create", methods=["GET"])
@cross_origin()
def create_game():
    g.db.execute("INSERT INTO games(start_time, user_num) VALUES ((SELECT DATETIME(DATETIME('NOW', 'LOCALTIME'), '+5 SECONDS')), ?)", [1])
    g.db.commit()
    game_tuple = g.db.execute("SELECT id, max(start_time), user_num FROM games WHERE start_time >= (SELECT DATETIME('NOW', 'LOCALTIME'))").fetchone()
    game_dict = dict(id=game_tuple[0], start_time=game_tuple[1], user_num=game_tuple[2])
    return {"data": game_dict}


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
