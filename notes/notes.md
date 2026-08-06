HTML
 │
 ▼
BeautifulSoup -> responsible for creation of dom tree
 │
 ▼
Extract:
    • title -> x.title.string
    • text -> x.get_text(seperator=" ", strip = True)
    • links -> links [] | loop in thsi by find_all("a") -> href = 
 │
 ▼
Page Object

CRAWLER ALGO

Start with one URL.

Put it in a queue.

While the queue is not empty:

    Take one URL.

    If already visited:
        Skip it.

    Download the page.

    Parse the page.

    Save the page.

    Mark it as visited.

    Add every new link to the queue.

Repeat until we've crawled enough pages.