from fastapi import FastAPI
from crawler import Crawler
from indexer import Indexer
from search_engine import SearchEngine
from snippet import SnippetGenerator

app = FastAPI()


SITES = [
    (
        "https://en.wikipedia.org/wiki/Main_Page",
        {"en.wikipedia.org"}
    ),
    (
        "https://developer.mozilla.org/",
        {"developer.mozilla.org"}
    ),
    (
        "https://docs.python.org/3/",
        {"docs.python.org"}
    ),
    (
        "https://docs.oracle.com/en/java/",
        {"docs.oracle.com"}
    ),
    (
        "https://www.gnu.org/",
        {"www.gnu.org"}
    )
]


crawler = Crawler()
indexer = Indexer()
snippet_generator = SnippetGenerator()

pages = []


# Crawl all configured websites
for seed_url, allowed_domains in SITES:

    print(f"Crawling: {seed_url}")

    site_pages = crawler.crawl(
        seed_url=seed_url,
        max_pages=10,
        max_depth=2,
        allowed_domains=allowed_domains
    )

    print(f"Crawled {len(site_pages)} pages")

    pages.extend(site_pages)


print(f"Total pages crawled: {len(pages)}")


# Build one combined index
index = indexer.build(pages)

print(f"Indexed {len(index)} unique words")


# Create search engine using all pages
search_engine = SearchEngine(
    pages,
    index
)


@app.get("/search")
def search(
    query: str,
    page: int = 1,
    page_size: int = 10
):

    if page < 1:
        page = 1

    if page_size < 1:
        page_size = 10

    results = search_engine.search(query)

    total_results = len(results)

    start = (page - 1) * page_size
    end = start + page_size

    paginated_results = results[start:end]

    total_pages = (
        (total_results + page_size - 1)
        // page_size
    )

    return {
        "query": query,
        "page": page,
        "page_size": page_size,
        "total_results": total_results,
        "total_pages": total_pages,
        "results": [
            {
                "title": result["page"].title,
                "url": result["page"].url,
                "score": result["score"],
                "snippet": snippet_generator.generate(
                    result["page"].text,
                    query
                )
            }
            for result in paginated_results
        ]
    }