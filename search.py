import argparse
import concurrent.futures
from requests.exceptions import Timeout
from logzero import logger
from libs import Evil, is_alive, Ahmia, Torch

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ReconTor")
    parser.add_argument("--search", help="query to search for", required=True)
    parser.add_argument("--file", help="output file name", required=True)
    parser.add_argument(
        "--threads", help="increase threads default 5", default=5, type=int)
    parser.add_argument("--title", help="save title with url ':' delimited",
                        default=False, action="store_true")
    parser.add_argument("--evil", help="search on not_evil much slower",
                        default=False, action="store_true")
    args = parser.parse_args()
    search = args.search
    found = []

    if args.evil:
        try:
            evil = Evil()
            evil.search(search)
            logger.info(f'found {len(evil.found)} from not_evl')
            found = {*found, *evil.found}
        except Exception as e:
            logger.error('Evil search failed')
            logger.exception(e)

    try:
        ahmia = Ahmia()
        ahmia.search(search)
        logger.info(f'found {len(ahmia.found)} from Ahmia')
        found = {*found, *ahmia.found}
    except Exception as e:
        logger.error('Ahmia search failed')
        logger.exception(e)

    try:
        torch = Torch()
        torch.threads = args.threads
        torch.search(search)
        logger.info(f'found {len(torch.found)} from Torch')
        found = {*found, *torch.found}
    except Exception as e:
        logger.error('torch search failed')
        logger.exception(e)

    logger.info(f'found {len(found)} onions relating to {search}')
    f = open(args.file, 'a')
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_url = {executor.submit(is_alive, url): url for url in found}
        for future in concurrent.futures.as_completed(future_to_url):
            url: str = future_to_url[future]
            try:
                title: str = future.result().strip()
            except Timeout:
                logger.error(f'{url} timed out')
            except ConnectionError:
                logger.error(f'{url} failed to connect to host')
            except ValueError as e:
                logger.error(e)
            except Exception as exc:
                logger.error(f'some error with {url}')
            else:
                line = f'{url}:{title}\n' if args.title else f'{url}\n'
                logger.info(f'{url} {title}')
                f.write(line)
                f.flush()
    f.close()
