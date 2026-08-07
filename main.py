
from crawler import Crawler
from indexer import Indexer
from search_engine import SearchEngine


def main():
    # Step 1: Crawl websites
    crawler = Crawler()

    pages = crawler.crawl(
        "https://spring.io",
        max_pages=5
    )

    print(f"\nCrawled {len(pages)} pages")

    # Step 2: Build search index
    indexer = Indexer()
    index = indexer.build(pages)

    print(f"Indexed {len(index)} unique words")

    # Step 3: Create search engine
    engine = SearchEngine(pages, index)

    print("\n================================")
    print("       Simple Search Engine")
    print("================================")
    print("Type 'exit' to quit.\n")

    # Step 4: Keep accepting searches
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

            # Show only a small portion of page text
            print(f"   {page.text[:300]}...")
            print("-" * 60)

        print()


if __name__ == "__main__":
    main()

