import requests
from requests.structures import CaseInsensitiveDict


login_url = "https://prodigit.uniroma1.it/names.nsf?Login"
logout_url = "https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf?logout"
prenota_lezioni_url = "https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/prenotaposto-aula-lezioni"


credentials = {'Username': "qua",
            'Password': "qua"}

headers = CaseInsensitiveDict()
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
headers["Connection"] = "keep-alive"
headers["Content-Type"] = "application/x-www-form-urlencoded"

# LOGIN 

login = requests.post(login_url, data = credentials, headers = headers)

headers["Cookie"] = "LtpaToken="+login.request.headers['Cookie'][10:]


# PRENOTA AULA

click = "__Click=C12585E7003519C8.c8e9f943d3b2819fc12587ed0064a0a2%2F%24Body%2F2.9F0"
codice_edificio="codiceedificio=RM018"
aula="aula=AULA+1+--+RM018-E01PTEL013"
dalleore="dalleore2=08%3A00"
alleore="alleore2=09%3A00"

parameters = [click, codice_edificio, aula, dalleore, alleore]
data = ""
for param in parameters:
    data+=param+"&"

resp = requests.post(prenota_lezioni_url, headers=headers, data=data)

# LOGOUT
logout = requests.post(logout_url)
print(logout.status_code)