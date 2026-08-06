from crawler import Crawler


def main():

    crawler = Crawler()

    pages = crawler.crawl(
        "https://spring.io",
        max_pages=5
    )

    print(f"Crawled {len(pages)} pages\n")

    for page in pages:
        print("Title")
        print(page.title)
        print(page.url)
        print("-" * 40)

        print("Text")
        print(page.text[:300])


if __name__ == "__main__":
    main()