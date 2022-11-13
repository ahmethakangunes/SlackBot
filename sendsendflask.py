from flask import Flask, request, jsonify
from flask import jsonify
import sys
import json
from belge import get_access_token
from belge import belge
from blackhole import getmails
from info import getinfo
app = Flask(__name__)

@app.route("/belge", methods=['POST'])
async def docx():
    token = get_access_token()
    list = belge(request.json['login'], token)
    return list[1].title()

@app.route("/clear", methods=['POST'])
async def clear():
    token = get_access_token()
    mails = getmails(token)
    return (mails)

@app.route("/info", methods=['POST'])
async def info():
    token = get_access_token()
    info = getinfo(request.json['login'], token)
    return "200"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=2424)