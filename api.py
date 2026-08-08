from fastapi import FastAPI, Query
from crawler import Crawler
from search_engine import SearchEngine


from indexer import Indexer
from search_engine import SearchEngine

app = FastAPI(
    title="DevSearch API",
    description="A simple web search engine",
    version="1.0.0"
)

query = str(input("Enter the query"))

crawler = Crawler()
pages = crawler.crawl( "https://spring.io", max_pages=5 )

indexer = Indexer()
index = indexer.build(pages)

search = SearchEngine()
engine = search.search(query)
