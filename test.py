import requests
import time
import pandas as pd
import dateutil.parser
from datetime import datetime
import sys
from sys import argv

def day(lastseen):
    if (lastseen != None):
        lastday = datetime.strptime(lastseen,"%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.now().strptime(now, "%Y-%m-%d %H:%M:%S")
        lastseen = str(lastday - now)
        li = list(lastseen.split(" "))
        print(li)
        if (len(li) == 1):
            return (0)
        return(int(li[0]))

def location(login, token):
    headers = {
    'Authorization': 'Bearer ' + token,
    }
    endpoint = f"/v2/users/{login}/locations"
    response = requests.get('https://api.intra.42.fr' + "{}".format(endpoint), headers=headers)
    responsejs = response.json()
    return (day(responsejs[0]['end_at']))

def getday(token):
    count = 0
    pagenumber = 1
    list = []
    result = 0
    headers = {
    'Authorization': 'Bearer ' + token,
    }
    params = {
            "page[size]": 100, 
            "sort":"id" , 
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
                if (result > 0):
                    campuslog = location(responsejs[i]['user']['login'], token)
                    if (campuslog >= -7):
                        campuslog *= -1
                        print(responsejs[i]['user']['login'], str(campuslog), "gün önce geldi.", sep=" ")
                        count += 1
                    elif (campuslog == None):
                        print("Aktif:" + responsejs[i]['user']['login'], sep=" ")
                        count += 1
        pagenumber += 1




def get_access_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-05b797961e39f9ca81738308f9b2a7e2ed752549806393581cf56fc0685062bb", "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"),
  )
  return response.json()["access_token"]


token = get_access_token()
getday(token)