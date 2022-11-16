import requests

def part(file, responsejs):
    part = 1
    projectcount = 0
    examrank02 = 0
    examrank03 = 0
    for i in range(len(responsejs['projects_users'])):
        if (int(responsejs['projects_users'][i]['project']['id']) < 1314):
          file.write("Part: 1" + "\n")
          break
        status = responsejs['projects_users'][i]['status']
        point = responsejs['projects_users'][i]['final_mark']
        if (status == "finished" and int(point) > 75):
          projectcount += 1
          project = responsejs['projects_users'][i]['project']['name']
          if (project == "Exam Rank 02"):
            examrank02 += 1
          if (project == "Exam Rank 03"):
            examrank03 += 1
          if (examrank02 == 1 and projectcount >= 8):
              part = 2
          if (examrank03 == 1 and projectcount >= 22):
              part = 3
          if (project == "Libft"):       
            file.write("Part: " + str(part) + "\n")
            break

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
            print(responsejs[i]['user']['login'])
        pagenumber += 1


def get_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-ad74f3208071d0a40ffd78a2a0a7abc0562e35c85d9343c71717f7bfb5565f95", "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"),
  )
  return response.json()["access_token"]


token = get_token()
file = open("part3.txt", "a+")
part(file)