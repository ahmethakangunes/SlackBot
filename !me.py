import requests
import time
import dateutil.parser
from datetime import datetime
import sys
from sys import argv

def day(file, blackhole):
    lastday = datetime.strptime(blackhole,"%Y-%m-%dT%H:%M:%S.%fZ")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.now().strptime(now, "%Y-%m-%d %H:%M:%S")
    blackhole = str(lastday - now)
    li = list(blackhole.split())
    file.write("Black Hole: " + str(li[0]) + " gün ")
    li = li[2].split(":")
    print((int(li[0])))
    file.write(li[0] + " saat " + li[1] + " dakika " + li[2] + " saniye" + "\n")
  

def getinfo(login, token):
    headers = {
    'Authorization': 'Bearer ' + token,
    }
    endpoint = "/v2/users/{}".format(login)
    response = requests.get('https://api.intra.42.fr' + "{}".format(endpoint), headers=headers)
    if (response.status_code == 200):
      responsejs = response.json()
      file = open(("info/" + login + ".txt"), "w")
      file.write("Selam " + str(responsejs['first_name']).title() + "bilgilerini getirdim.\n")
      file.write("Ad: " + str(responsejs['first_name']).title() + "\n")
      file.write("Soyad: " + str(responsejs['last_name']).title() + "\n")
      file.write("Login: " + str(responsejs['login']) + "\n")
      day(file, responsejs['cursus_users'][1]['blackholed_at'])
      file.write("Wallet: " + str(responsejs['wallet']) + "\n")
      file.write("Intra: " + "https://profile.intra.42.fr/users/" + str(responsejs['login']) + "\n")
    else:
      exit (1)
    

def get_access_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-05b797961e39f9ca81738308f9b2a7e2ed752549806393581cf56fc0685062bb", "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"),
  )
  return response.json()["access_token"]

token = get_access_token()
getinfo(sys.argv[1], token)