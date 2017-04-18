import logging
import sys
import re
import json
import asyncio
import aiohttp
from time import sleep
from lxml import html

__author__ = "Andrew Gafiychuk"


class Parser(object):

    def __init__(self, page_count):
        self.pages = page_count
        self.session = None

    async def prepare(self):
        logging.debug("[+]Create HEADERS/Sessions...")

        HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,uk;'
                               'q=0.2',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'forum.overclockers.ua',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/57.0.2987.133'
                          'Safari/537.36',
        }

        connector = aiohttp.TCPConnector(verify_ssl=True)
        self.session = aiohttp.ClientSession(connector=connector, headers=HEADERS)

        logging.debug("[+]Session created !!!")
        return

    def urls_get(self):
        URL = 'http://forum.overclockers.ua/viewforum.php?f=26&start={0}'

        urls = []

        start = 0
        for url in range(0, self.pages):
            urls.append(URL.format(start))
            start += 40

        return urls

    def start(self):
        logging.debug("[+]Starts main even_loop...")

        event_loop = asyncio.get_event_loop()

        try:
            event_loop.run_until_complete(self.prepare())
            results = event_loop.run_until_complete(self.main())
        except Exception as err:
            logging.debug("[+]Even_loop some error...\n"
                          "{0}".format(err))
        finally:
            logging.debug("[+]All coroutines complete !!!\n"
                          "[+]Close session/event_loop !!!")

            self.session.close()
            event_loop.close()

        return results

    async def main(self):
        logging.debug("[+]Starting all tasks...")

        urls = self.urls_get()

        tasks = []
        results = []

        for url in urls:
            tasks.append(self.fetch_url(url))

        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
            task.close()

        logging.debug("[+]All tasks complete !!!")
        return results

    async def fetch_url(self, url):
        async with self.session.get(url) as response:
            if response.status == 200:
                print("URL: {0} fetch complete !!!".format(url))
                html = await response.text()
                return html
            else:
                logging.debug("[+]URL get error...")

    @staticmethod
    async def parse_and_save_page(html):
        root = html.fromstring(html)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("[+]App started...")

    parser = Parser(10)
    results = parser.start()

    for result in results:
        print(result)
        sleep(3)

    logging.debug("[+]App done !!!")