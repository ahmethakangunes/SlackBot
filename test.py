from flask import Flask, request, jsonify
from flask import jsonify
import sys
import json
from belge import get_access_token
from belge import belge
from blackhole import getmails
app = Flask(__name__)

@app.route("/belge", methods=['POST'])
def docx():
    token = get_access_token()
    print(request.json['login'], token)
    list = belge(request.json['login'], token)
    return list[1].title()

@app.route("/clear", methods=['POST'])
def clear():
    token = get_access_token()
    return (getmails(token))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2424)