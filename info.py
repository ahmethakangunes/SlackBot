import requests
import time
import dateutil.parser
from datetime import datetime
import sys
from sys import argv



part1projects = ["Libft", "get_next_line", "ft_printf", "Born2beroot", "push_swap", "Exam Rank 02", "minitalk", "so_long", "pipex", "FdF", "fract-ol"]
part2projects = ["minishell", "Exam Rank 03", "Philosophers", "NetPractice", "cub3d", "miniRT", "CPP Module 00", "CPP Module 01", "CPP Module 02", "CPP Module 03", "CPP Module 04", "CPP Module 05", "CPP Module 06", "CPP Module 07", "CPP Module 08", "Exam Rank 04"]
part3projects = ["webserv", "ft_irc", "ft_containers", "Exam Rank 05", "ft_transcendence", "Exam Rank 06", "Inception"]

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

def part(file, responsejs):
	global part1projects, part2projects, part3projects
	part = 1
	projectcount = 0
	part1count = 0
	part2count = 0
	for i in range(len(responsejs['projects_users'])):
		validated = responsejs['projects_users'][i]['validated?']
		projectname = responsejs['projects_users'][i]['project']['name']
		if (validated == True):
			if (projectname in part1projects):
				part1count += 1
			elif (projectname in part2projects):
				part2count += 1
			if (part1count >= 8 and part2count < 15):
				part = 2
			if (part1count >= 8 and part2count >= 15):
				part = 3
	file.write("Part: " + str(part) + "\n")



def project(file, responsejs):
	global projectlist
	file.write("-" * 40 + " Projeler " + "-" * 40 + "\n")
	for i in range(len(responsejs['projects_users'])):
		cursus_ids = responsejs['projects_users'][i]['cursus_ids']
		validated = responsejs['projects_users'][i]['validated?']
		if (validated == True and cursus_ids[0] == 21):
			point = responsejs['projects_users'][i]['final_mark']
			project = responsejs['projects_users'][i]['project']['name']
			time = responsejs['projects_users'][i]['updated_at']
			reversetime = datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
			reversetime = str(reversetime).split(" ")
			day = day2(time)
			file.write("Proje: " +  str(project) + " Puan: " + str(point) + " Teslim Tarihi: " + \
				str(reversetime[0].replace("-", ".")) + " Geçen zaman: " + str(day) + "\n")


def getinfo(login, token):
	headers = {
	'Authorization': 'Bearer ' + token,
	}
	endpoint = "/v2/users/{}".format(login)
	response = requests.get('https://api.intra.42.fr' + "{}".format(endpoint), headers=headers)
	if (response.status_code == 200):
		responsejs = response.json()
		file = open("info/" + login + ".txt", "w")
		file.write("Selam, " + str(responsejs['login']) + " kullanıcısının bilgilerini getirdim." + "\n" * 2)
		file.write("Ad: " + str(responsejs['first_name']).title() + "\n")
		file.write("Soyad: " + str(responsejs['last_name']).title() + "\n")
		file.write("Login: " + str(responsejs['login']) + "\n")
		part(file, responsejs)
		file.write("Intra: " + "https://profile.intra.42.fr/users/" + str(responsejs['login']) + "\n")
		day(file, responsejs['cursus_users'][1]['blackholed_at'])
		file.write("Wallet: " + str(responsejs['wallet']) + "\n")
		file.write("Masa: " + str(responsejs['cursus_users'][1]['user']['location']) + "\n")
		if (responsejs['cursus_users'][0]['user']['pool_year'] != None):
			file.write("Havuz Yılı: " + str(responsejs['cursus_users'][0]['user']['pool_year']) + "\n")
		else:
			file.write("Havuz: Havuz bilgisi bulunamadı" + "\n")
		project(file, responsejs)
	else:
		exit (1)

def get_access_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-xxxx", "s-s4t2ud-xxxx"),
  )
  return response.json()["access_token"]

token = get_access_token()
getinfo("aerdol", token)