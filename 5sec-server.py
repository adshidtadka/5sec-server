from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/result', methods=["POST"])
@cross_origin()
def result():
    user_name = request.form["userName"]
    result = request.form["result"]

    return result


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
