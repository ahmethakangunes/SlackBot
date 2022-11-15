import requests
import sys
from sys import argv
import pandas as pd

def personalmails(login):
    df = pd.read_excel('mails.xlsx')
    df.dropna(inplace = True)
    searchindex = (df.loc[df['byalcink'] == login])
    tolist = searchindex.values.tolist()
    if (len(tolist) > 0):
        mail = tolist[0][1]
        return mail
    else:
        return "ahmethakangunessds24@gmail.com"

def aguinfo(login, token, slackmail):
  personalmail = personalmails(login)
  if (slackmail != personalmail):
      return ("false")
  return ("asdddsasdasd")

def get_access_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-05b797961e39f9ca81738308f9b2a7e2ed752549806393581cf56fc0685062bb", "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"),
  )
  return response.json()["access_token"]
