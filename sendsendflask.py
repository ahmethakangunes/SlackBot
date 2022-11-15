from flask import Flask, request, jsonify
from flask import jsonify
import sys
import json
from agu import aguinfo
from belge import get_access_token
from ratelimit import limits
from belge import belge
from blackhole import getmails
from info import getinfo
app = Flask(__name__)

@app.route("/belge", methods=['POST'])
@limits(calls=1, period=1)
def docx():
    login = request.json['login']
    slackmail = request.json['mail']
    token = get_access_token()
    list = belge(login, token, slackmail)
    return list[1].title()

@limits(calls=1, period=1)
@app.route("/agu", methods=['POST'])
async def agu():
    login = request.json['login']
    slackmail = request.json['mail']
    token = get_access_token()
    list = aguinfo(login, token, slackmail)
    return (list[1].title())

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
