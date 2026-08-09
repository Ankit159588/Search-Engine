from fastapi import FastAPI
from crawler import Crawler
from indexer import Indexer
from search_engine import SearchEngine

app = FastAPI()
crawler = Crawler()
indexer = Indexer()

pages = crawler.crawl(
    "https://spring.io",
    max_pages=10
)

index = indexer.build(pages)

search_engine = SearchEngine(
    pages,
    index
)

@app.get("/search")
def search(query: str):

    results = search_engine.search(query)

    return {
        "query": query,
        "results": [
            {
                "title": result["page"].title,
                "url": result["page"].url,
                "score": result["score"]
            }
            for result in results
        ]
    }