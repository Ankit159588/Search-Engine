from downloader import Downloader
from parser import Parser
from collections import deque
from urllib.parse import urlparse


class Crawler:

    def __init__(self):
        self.downloader = Downloader()
        self.parser = Parser()

    def crawl(
        self,
        seed_url,
        max_pages=10,
        max_depth=2,
        allowed_domains=None
    ):

        queue = deque([(seed_url, 0)])
        queued = {seed_url}

        visited = set()
        pages = []

        while queue and len(pages) < max_pages:

            url, depth = queue.popleft()

            if url in visited:
                continue

            if allowed_domains:
                domain = urlparse(url).netloc

                if domain not in allowed_domains:
                    continue

            html = self.downloader.download(url)

            if html is None:
                continue

            visited.add(url)

            page = self.parser.parse(url, html)
            pages.append(page)

            # Don't discover deeper pages
            if depth >= max_depth:
                continue

            for link in page.links:

                if link in visited or link in queued:
                    continue

                if allowed_domains:
                    link_domain = urlparse(link).netloc

                    if link_domain not in allowed_domains:
                        continue

                queue.append((link, depth + 1))
                queued.add(link)

        return pages