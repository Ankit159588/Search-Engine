
import math
from tokenizer import Tokenizer


class Ranker:

    def __init__(self, pages, index):

        self.pages = pages
        self.index = index

        self.tokenizer = Tokenizer()

        self.document_lengths = []

        for page in pages:
            length = len(self.tokenizer.tokenize(page.text))
            self.document_lengths.append(length)

        if self.document_lengths:
            self.average_document_length = (
                sum(self.document_lengths)
                / len(self.document_lengths)
            )
        else:
            self.average_document_length = 0

    def score(self, word, page_id, tf):

        total_documents = len(self.pages)

        postings = self.index.get(word, {})
        document_frequency = len(postings)

        if total_documents == 0:
            return 0

        if document_frequency == 0:
            return 0

        document_length = self.document_lengths[page_id]

        if self.average_document_length == 0:
            return 0

        # BM25 parameters
        k1 = 1.5
        b = 0.75

        # IDF
        idf = math.log(
            1 + (
                (total_documents - document_frequency + 0.5)
                / (document_frequency + 0.5)
            )
        )

        # Document length normalization
        length_normalization = (
            1 - b
            + b * (
                document_length
                / self.average_document_length
            )
        )

        # Term frequency score
        term_score = (
            (tf * (k1 + 1))
            / (
                tf
                + k1 * length_normalization
            )
        )

        score = idf * term_score

        # Tokenize the page title
        title_words = self.tokenizer.tokenize(
            self.pages[page_id].title
        )

        # Give extra importance to an exact title word
        if word in title_words:
            score *= 2

        return score


    def phrase_score(self, query, page_id):

        query_words = self.tokenizer.tokenize(query)

        # Phrase matching only makes sense for 2+ words
        if len(query_words) < 2:
            return 0

        page_words = self.tokenizer.tokenize(
            self.pages[page_id].text
        )

        title_words = self.tokenizer.tokenize(
            self.pages[page_id].title
        )

        phrase_length = len(query_words)

        body_matches = 0
        title_matches = 0

        # Count exact phrase occurrences in body
        for i in range(
                len(page_words) - phrase_length + 1
        ):
            if page_words[
                i:i + phrase_length
            ] == query_words:
                body_matches += 1

        # Count exact phrase occurrences in title
        for i in range(
                len(title_words) - phrase_length + 1
        ):
            if title_words[
                i:i + phrase_length
            ] == query_words:
                title_matches += 1

        # Body phrase gets a small boost
        body_score = body_matches * 1

        # Title phrase gets a much stronger boost
        title_score = title_matches * 5

        return body_score + title_score





