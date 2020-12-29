import requests


class WebSession:
    session = requests.Session()
    is_authorized = False


url = "http://127.0.0.1:8000"
session = WebSession()
