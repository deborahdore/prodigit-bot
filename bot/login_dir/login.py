import requests

from bot.utility import create_headers

login_url = "https://prodigit.uniroma1.it/names.nsf?Login"


def login(username, password):
    headers = create_headers()
    credentials = {'Username': username,
                   'Password': password}
    login = requests.post(login_url, data=credentials, headers=headers)

    try:
        return "LtpaToken=" + login.request.headers['Cookie'][10:]
    except:
        return ""
