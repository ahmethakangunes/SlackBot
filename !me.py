import requests
import time
import dateutil.parser
import pandas as pd
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

def day(file, blackhole):
    if (blackhole != None):
      lastday = datetime.strptime(blackhole,"%Y-%m-%dT%H:%M:%S.%fZ")
      now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      now = datetime.now().strptime(now, "%Y-%m-%d %H:%M:%S")
      blackhole = str(lastday - now)
      li = list(blackhole.split())
      if (int(li[0]) > 0):
        file.write("Black Hole: " + str(li[0]) + " gün ")
        li = li[2].split(":")
        file.write(li[0] + " saat " + li[1] + " dakika " + li[2] + " saniye" + "\n")
      else:
        li[0] = (int(li[0]) * -1)
        file.write("Black Hole: " + str(li[0]) + " gün ")
        li = li[2].split(":")
        file.write(li[0] + " saat " + li[1] + " dakika " + li[2] + " saniye önce aramızdan ayrıldı...\n")
        return(li[0])
    else:
      file.write("Black Hole: Mezun" + "\n")
  
  
def day2(time):
    lastday = datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%fZ")
    now = datetime.now().strptime(now, "%Y-%m-%d %H:%M:%S.%fZ")
    time = str(now - lastday)
    li = list(time.split())
    if (len(li) < 2):
      li = (li[0].split(":"))
      return (li[0] + " saat")
    return(li[0] + " gün")

def project(file, responsejs):
    file.write("\n" + "-" * 40 + " Projeler " + "-" * 40 + "\n")
    for i in range(len(responsejs['projects_users'])):
        status = responsejs['projects_users'][i]['status']
        point = responsejs['projects_users'][i]['final_mark']
        if (status == "finished" and int(point) > 75):
          project = responsejs['projects_users'][i]['project']['name']
          time = responsejs['projects_users'][i]['updated_at']
          reversetime = datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
          reversetime = str(reversetime).split(" ")
          day = day2(time)
          file.write("Proje: " +  str(project) + " Puan: " + str(point) + " Teslim Tarihi: " + str(reversetime[0].replace("-", ".")) + " Geçen zaman: " + str(day) + "\n")
          if (project == "Libft"):
            break
          
def location(login, file):
    headers = {
    'Authorization': 'Bearer ' + token,
    }
    endpoint = f"/v2/users/{login}/locations"
    response = requests.get('https://api.intra.42.fr' + "{}".format(endpoint), headers=headers)
    responsejs = response.json()
    if (len(responsejs) == 0):
      return ("Masa: Aktif değil" + "\n")
    else:
      if (responsejs[0]['end_at'] == None):
          file.write("Masa: " + str(responsejs[0]['host']) + "\n")
      else:
          file.write("Masa: Aktif değil" + "\n")

def getinfo(login, slackmail, token):
    personalmail = personalmails(login)
    if (slackmail != personalmail):
        print ("Hata")
        return
    else:
      print("OK")
    headers = {
    'Authorization': 'Bearer ' + token,
    }
    endpoint = "/v2/users/{}".format(login)
    response = requests.get('https://api.intra.42.fr' + "{}".format(endpoint), headers=headers)
    if (response.status_code == 200):
      responsejs = response.json()
      file = open(("me/" + login + ".txt"), "w")
      file.write("Selam, " + str(responsejs['usual_full_name']) + " bilgilerini getirdim." + "\n" * 2)
      file.write("Ad: " + str(responsejs['first_name']).title() + "\n")
      file.write("Soyad: " + str(responsejs['last_name']).title() + "\n")
      file.write("Login: " + str(responsejs['login']) + "\n")
      file.write("Intra: " + "https://profile.intra.42.fr/users/" + str(responsejs['login']) + "\n")
      day(file, responsejs['cursus_users'][1]['blackholed_at'])
      file.write("Wallet: " + str(responsejs['wallet']) + "\n")
      location(login, file)
      if (responsejs['cursus_users'][0]['user']['pool_year'] != None):
        file.write("Havuz: " + str(responsejs['cursus_users'][0]['user']['pool_year']))
      else:
        file.write("Havuz: Havuz bilgisi bulunamadı" + "\n")
      project(file, responsejs)
    else:
      print(response.status_code)
    

def get_access_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-05b797961e39f9ca81738308f9b2a7e2ed752549806393581cf56fc0685062bb", "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"),
  )
  return response.json()["access_token"]

token = get_access_token()
getinfo(sys.argv[1], sys.argv[2],token)