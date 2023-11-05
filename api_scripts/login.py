import typing

import requests
from bs4 import BeautifulSoup

url = "http://localhost:8080"


def get_session(url, username, password):
    sess = requests.Session()

    r = sess.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    token_tags = soup.find_all(attrs={"name": "csrf_token"})
    token_tag = token_tags[0]
    csrf_token = token_tag["value"]

    payload = {"username": username, "password": password, "csrf_token": csrf_token}

    _ = sess.post(r.url, data=payload)

    return sess


class AirflowLogin:
    def __init__(
        self, url: str, username: str, password: str, get_session: typing.Callable
    ) -> None:
        self._url = url

        self._username = username
        self._password = password

        self._session = None

        self._get_session = get_session

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, _type, value, traceback):
        self.close()

    def login(self):
        self._session = self._get_session(self._url, self._username, self._password)
        return self

    def close(self):
        self._session.close()
        self._session = None
