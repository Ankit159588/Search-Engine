from bs4 import BeautifulSoup
from page import Page
from urllib.parse import urljoin

class Parser:

    def parse (self, url: str, html: str) -> Page:
        # page has 4 things title, text, link
        soup = BeautifulSoup(html, "lxml") # creation of DOM tree
        #text extracton 
        text = soup.get_text(separator=" ", strip=True)
        # title extraction
        title = soup.title.string if soup.title else " "


        # links extraction
        links = set()
        for link in soup.find_all("a"):
            href = link.get("href")

            if not href:
                continue
            if href.startswith("#"):
                continue
            if href.startswith("mailto:"):
                continue
            if href.startswith("javascript:"):
                continue

            absolute_url = urljoin(url, href)
            links.add(href)

        return Page(url = url, title = title, text = text, links = links)