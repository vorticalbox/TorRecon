import re
from typing import List
from logzero import logger
from libs.helpers import session, bs


class Ahmia:
    timeout: int
    found: List[str] = []

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def search(self, term: str):
        logger.info(f'Searching ahmia for {term}')
        r = session.get(f'https://ahmia.fi/search/?q={term}').text
        soup = bs(r, features="html5lib")
        for link in soup.findAll('a'):
            href = link.get('href')
            if 'redirect_url' in href:
                self.found.append(re.search(r"redirect_url=(.+)", href).group(1))