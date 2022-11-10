import requests
import sys
from sys import argv

def agu(login, process):
    file = open(("agu/" + login + ".txt"), "w")
    if (process == "işlemde"):
      file.write("Talep durumu: İşlemde.")
    elif (process == "finish"):
      file.write("Talep durumu: Sonuçlandı, lütfen mail adresinizi kontrol ediniz.")
    else:
      exit(1)
    
def user(login, token, process):
    headers = {
    'Authorization': 'Bearer ' + token,
    }
    endpoint = "/v2/users/{}".format(login)
    response = requests.get('https://api.intra.42.fr' + "{}".format(endpoint), headers=headers)
    if (response.status_code == 200):
        agu(login, process)
    else:
        exit(1)
    

def get_access_token():
  response = requests.post(
    "https://api.intra.42.fr/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=("u-s4t2ud-05b797961e39f9ca81738308f9b2a7e2ed752549806393581cf56fc0685062bb", "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"),
  )
  return response.json()["access_token"]

login = sys.argv[1]
process = sys.argv[2]
token = get_access_token()
user(login, token, process)