import requests
import time
import pandas as pd
import dateutil.parser
from datetime import datetime
import sys
from sys import argv

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

def day(blackhole):
    if (blackhole != None and blackhole != "None"):
        lastday = datetime.strptime(blackhole,"%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.now().strptime(now, "%Y-%m-%d %H:%M:%S")
        blackhole = str(lastday - now)
        li = list(blackhole.split(" "))
        if (len(li) == 1):
            return (0)
        return(int(li[0]))
    else:
        return (1)

def getmails(token):
    pagenumber = 1
    list = []
    result = 0
    headers = {
    'Authorization': 'Bearer ' + token,
    }
    params = {
            "page[size]": 100, 
            "sort":"blackholed_at" , 
            "filter[campus_id]": 49,
    }
    while True:
        endpoint = f"/v2/cursus/21/cursus_users?page[number]={pagenumber}"
        response = requests.get('https://api.intra.42.fr' + "{}".format(endpoint), headers=headers, params=params)
        responsejs = response.json()
        for i in range(len(responsejs)):
           if (responsejs[i]['user']['kind'] == "student"):
                time.sleep(0.5)
                result = day(responsejs[i]['blackholed_at'])
                if (result < 0):
                    if (responsejs[i]['user']['active?'] == False):
                        list.append(personalmails(responsejs[i]['user']['login']))
                else:
                    return (list)
        pagenumber += 1

def get_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-05b797961e39f9ca81738308f9b2a7e2ed752549806393581cf56fc0685062bb", "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"),
  )
  return response.json()["access_token"]
