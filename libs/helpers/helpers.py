import requests
from bs4 import BeautifulSoup as bs

session = requests.session()
proxies = {"http": "socks5h://localhost:9050",
           "https": "socks5h://localhost:9050"}
session.proxies = proxies
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'
}


def is_alive(url) -> str:
    r = session.get(url, timeout=30)
    if r.status_code < 300 and r.text is not None:
        soup = bs(r.text, features="html5lib")
        return soup.title.string if soup.title else 'N/A'

    raise ValueError(f'{url=} {r.status_code=}')
