import requests
from requests.exceptions import RequestException

class Downloader:
    # def download(self, url: str):
    #     response = requests.get(url)
    #     return response.text

    def download(self, url: str):
        header = {
            "User-Agent": "DevSearchBot/1.0"
        }

        try: 
            response = requests.get(url, headers=header, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"Failed to download {url}")
            print(e)
            return None