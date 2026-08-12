from crawler import Crawler
from indexer import Indexer
from search_engine import SearchEngine


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


def main():

    # Step 1: Crawl all websites
    crawler = Crawler()

    pages = []

    for seed_url, allowed_domains in SITES:

        print(f"\nCrawling: {seed_url}")

        site_pages = crawler.crawl(
            seed_url=seed_url,
            max_pages=20,
            max_depth=2,
            allowed_domains=allowed_domains
        )

        print(f"Crawled {len(site_pages)} pages")

        pages.extend(site_pages)

    print(f"\nTotal pages crawled: {len(pages)}")

    # Step 2: Build search index
    indexer = Indexer()

    index = indexer.build(pages)

    print(f"Indexed {len(index)} unique words")

    # Step 3: Create search engine
    engine = SearchEngine(pages, index)

    print("\n================================")
    print("       DevSearch")
    print("================================")
    print("Search across:")
    print("Wikipedia")
    print("MDN")
    print("Python Docs")
    print("Oracle Java Docs")
    print("GNU")
    print("\nType 'exit' to quit.\n")

    # Step 4: Search loop
    while True:

        query = input("Search: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            print("Please enter a search query.\n")
            continue

        # Step 5: Search
        results = engine.search(query)

        print(f"\nFound {len(results)} results\n")

        if not results:
            print("No results found.\n")
            continue

        # Step 6: Display results
        for number, result in enumerate(results, start=1):

            page = result["page"]
            score = result["score"]

            print(f"{number}. {page.title}")
            print(f"   URL: {page.url}")
            print(f"   Score: {score:.4f}")
            print(f"   {page.text[:300]}...")
            print("-" * 60)

        print()


if __name__ == "__main__":
    main()