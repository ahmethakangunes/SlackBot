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
    auth=("u-s4t2ud-ad74f3208071d0a40ffd78a2a0a7abc0562e35c85d9343c71717f7bfb5565f95", "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"),
  )
  return response.json()["access_token"]
