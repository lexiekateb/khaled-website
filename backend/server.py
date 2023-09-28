from flask import Flask, jsonify, request
from flask_cors import CORS

x = "hello, this works!"

app = Flask(__name__)
CORS(app)

@app.route("/", methods = ['POST'])

def hello():
    in_json = request.get_json(force=True)
    sum = int(in_json['p0']) + int(in_json['p1']) + int(in_json['p2']) + int(in_json['p3']) + int(in_json['p4'])
    return {'sum': sum}


if __name__ == "__main__":
    app.run(debug=True)