import requests
import sys
from sys import argv
import pandas as pd

def personalmails(login):
    df = pd.read_excel('xxxx.xlsx')
    df.dropna(inplace = True)
    searchindex = (df.loc[df['xxxx'] == login])
    tolist = searchindex.values.tolist()
    if (len(tolist) > 0):
        mail = tolist[0][1]
        return mail
    else:
        return "ahmethakangunsdessds24@gmail.com"

def examlogin(login, token, slackmail):
  personalmail = personalmails(login)
  if (slackmail != personalmail):
      return 0
  else:
      return 1

def get_access_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-xxxx", "s-s4t2ud-xxxx"),
  )
  return response.json()["access_token"]
