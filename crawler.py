from downloader import Downloader
from parser import Parser
from collections import deque
from urllib.parse import urljoin

class Crawler:

    def __init__(self):
        self.downloader = Downloader()
        self.parser = Parser()

    def crawl(self, seed_url, max_pages=10):

        queue = deque([seed_url])
        visited = set()
        pages = []

        while queue and len(pages) < max_pages:

            url = queue.popleft()

            if url in visited:
                continue

            visited.add(url)

            html = self.downloader.download(url)

            if html is None:
                continue

            page = self.parser.parse(url, html)
            pages.append(page)

            for link in page.links:
                absolute_url = urljoin(url, link)
                if absolute_url not in visited:
                    queue.append(absolute_url)

        return pages