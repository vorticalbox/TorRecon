import concurrent.futures
from typing import List
from logzero import logger
from libs.helpers import session, bs


class Torch:
    url = 'http://cnkj6nippubgycuj.onion'
    timeout: int
    pages: List[str] = []
    term: str
    found = []
    threads = 5

    def __init__(self, timeout=30):
        self.timeout = timeout

    def search(self, term: str):
        self.term = term
        r = session.get(f'{self.url}/search?query={term}').text
        soup = bs(r, features="html5lib")
        pages = soup.find_all("a", class_="page-link")
        last = int(pages[-1].contents[0])
        for page in range(1, last):
            self.pages.append(f'{self.url}/search?query={self.term}&page={page}')
        logger.info(f'Torch: processing {len(self.pages)} pages')
        self.extract_links()

    def extract_link(self, page: str):
        r = session.get(page).text
        soup = bs(r, features="html5lib")
        count = 0
        for link in soup.find_all("a"):
            href = link.get('href')
            if href and 'http' in href and href not in self.found:
                self.found.append(href)
                count += 1
        return count

    def extract_links(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.extract_link, url): url for url in self.pages}
            for future in concurrent.futures.as_completed(future_to_url):
                url: str = future_to_url[future]
                try:
                    future.result()
                except Exception as exc:
                    logger.error(f'some error with {url}', exc)
