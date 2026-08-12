# class Page:
#     def __init__(self, url: str, title: str, text: str, links: list[str]):
#         self.url = url
#         self.title = title
#         self.text = text
#         self.links = links


from dataclasses import dataclass

@dataclass
class Page:
    url: str
    title: str
    text: str
    links: list[str]