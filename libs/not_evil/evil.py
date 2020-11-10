import re
from logzero import logger
from typing import List
from libs.helpers import session, bs


def extract_link(url: str):
    href = url.split('=')[1].replace('&q', '').replace('%3A', ':')
    address = re.sub('%2F', '/', href).split('.')
    return f'{address[0]}.onion'


class Evil:
    term: str
    timeout: int
    found: List[str]
    key: str

    def __init__(self, timeout: int = 30, found=None, ):
        if found is None:
            found = []
        self.timeout = timeout
        self.found = found

    def search(self, term: str):
        self.term = term
        logger.info(f'Searching not_evil for {self.term}')
        self.load_session()
        self.extract_links(f'http://hss3uro2hsxfogfq.onion/index.php?q={self.term}&session={self.key}&hostLimit=1', 0)

    def load_session(self):
        logger.info('getting session key')
        r = session.get('http://hss3uro2hsxfogfq.onion/index.php', timeout=30)
        soup = bs(r.text, features="html5lib")
        self.key = soup.find("input", {"name": "session"}).get('value')
        logger.info(f'Using session key {self.key}')

    def extract_links(self, url, last, pages=None):
        if pages is None:
            pages = []
        r = session.get(url, timeout=self.timeout).text
        soup = bs(r, features="html5lib")
        links = soup.findAll('a')
        token = None
        for link in links:
            href = link.get('href')
            if './index.php?q=' in href and token is None:
                token = re.search(r"session=(.{1,60})&", href).group(1)
            if 'r2d.php' in href:
                link = extract_link(href)
                if link not in self.found:
                    self.found.append(link)
        if len(pages) == 0:
            # extract the page links
            p = []
            for link in links:
                href = link.get('href')
                if './index.php?q=' in href:
                    p.append(f"http://hss3uro2hsxfogfq.onion{href.replace('./', '/')}")
            pages = list(set([int(re.search(r"start=([0-9]+)&", href).group(1)) for href in p]))
            pages.sort()
            logger.info(f'Processing {len(pages) - 1} pages')
        # generate the url
        next_url = f'http://hss3uro2hsxfogfq.onion/index.php?q={self.term}&session={token}&hostLimit=1&start={pages[last]}&numRows=20&template=0'
        next_index = last + 1
        # if we are not on the last page
        if next_index < len(pages):
            return self.extract_links(next_url, next_index, pages)
        return self.found
