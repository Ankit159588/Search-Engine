from bs4 import BeautifulSoup
from page import Page
from urllib.parse import urljoin


class Parser:

    def parse(self, url: str, html: str) -> Page:

        # Create DOM tree
        soup = BeautifulSoup(html, "lxml")

        # Extract text
        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Extract title
        title = soup.title.string if soup.title else ""

        # Extract links
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

            # Convert relative URL to absolute URL
            absolute_url = urljoin(url, href)

            links.add(absolute_url)

        return Page(
            url=url,
            title=title,
            text=text,
            links=links
        )