
from tokenizer import Tokenizer
from ranker import Ranker


class SearchEngine:

    def __init__(self, pages, index):
        self.pages = pages
        self.index = index
        self.ranker = Ranker(pages, index)
        self.tokenizer = Tokenizer()

    def search(self, query):

        words = self.tokenizer.tokenize(query)

        if not words:
            return []

        scores = {}

        for word in words:

            postings = self.index.get(word, {})

            for page_id, tf in postings.items():

                if page_id not in scores:
                    scores[page_id] = 0

                score = self.ranker.score(
                    word,
                    page_id,
                    tf
                )

                scores[page_id] += score

        # Apply phrase boost after calculating normal scores
        for page_id in scores:

            phrase_score = self.ranker.phrase_score(
                query,
                page_id
            )

            scores[page_id] += phrase_score

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        results = []

        for page_id, score in ranked:

            results.append({
                "page": self.pages[page_id],
                "score": score
            })

        return results

