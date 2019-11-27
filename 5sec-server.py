from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/')
@cross_origin()
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
