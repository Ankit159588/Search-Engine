from tokenizer import Tokenizer


class Indexer:

    def __init__(self):
        self.tokenizer = Tokenizer()

    def build(self, pages):

        index = {}

        for page_id, page in enumerate(pages):

            words = self.tokenizer.tokenize(page.text)

            for word in words:

                if word not in index:
                    index[word] = {}

                if page_id not in index[word]:
                    index[word][page_id] = 0

                index[word][page_id] += 1

        return index