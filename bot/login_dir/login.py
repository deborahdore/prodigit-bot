import requests
from requests.structures import CaseInsensitiveDict

login_url = "https://prodigit.uniroma1.it/names.nsf?Login"


def create_headers():
    headers = CaseInsensitiveDict()
    headers[
        "Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    headers["Connection"] = "keep-alive"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    return headers


def login(username, password):
    headers = create_headers()
    credentials = {'Username': username,
                   'Password': password}
    login = requests.post(login_url, data=credentials, headers=headers)

    try:
        return "LtpaToken=" + login.request.headers['Cookie'][10:]
    except:
        return ""
