import requests
from requests.exceptions import RequestException


class Downloader:

    def download(self, url):

        headers = {
            "User-Agent": "DevSearchBot/1.0"
        }

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            return response.content

        except RequestException as e:

            print(f"Failed to download {url}")
            print(e)

            return None