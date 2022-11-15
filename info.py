import requests
import time
import dateutil.parser
from datetime import datetime
import sys
from sys import argv

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
    file.write("-" * 40 + " Projeler " + "-" * 40 + "\n")
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
          
def location(login, file, token):
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

def getinfo(login, token):
    headers = {
    'Authorization': 'Bearer ' + token,
    }
    endpoint = "/v2/users/{}".format(login)
    response = requests.get('https://api.intra.42.fr' + "{}".format(endpoint), headers=headers)
    if (response.status_code == 200):
      responsejs = response.json()
      file = open(("info/" + login + ".txt"), "w")
      file.write("Selam, " + str(responsejs['login']) + " kullanıcısının bilgilerini getirdim." + "\n" * 2)
      file.write("Ad: " + str(responsejs['first_name']).title() + "\n")
      file.write("Soyad: " + str(responsejs['last_name']).title() + "\n")
      file.write("Login: " + str(responsejs['login']) + "\n")
      file.write("Intra: " + "https://profile.intra.42.fr/users/" + str(responsejs['login']) + "\n")
      day(file, responsejs['cursus_users'][1]['blackholed_at'])
      file.write("Wallet: " + str(responsejs['wallet']) + "\n")
      location(login, file, token)
      if (responsejs['cursus_users'][0]['user']['pool_year'] != None):
        file.write("Havuz: " + str(responsejs['cursus_users'][0]['user']['pool_year']))
        tsmonth = ts.google(str(responsejs['cursus_users'][0]['user']['pool_month']), from_language='en', to_language='tr').split(" ")[0].title()
        if (str(tsmonth) == "Aralik"):
            tsmonth = tsmonth.replace("i", "ı")
        file.write(" " + tsmonth + "\n")
      else:
        file.write("Havuz: Havuz bilgisi bulunamadı" + "\n")
      project(file, responsejs)
    else:
      exit (1)
