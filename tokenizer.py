import re


class Tokenizer:

    STOP_WORDS = {
        "a",
        "an",
        "the",
        "is",
        "are",
        "was",
        "were",
        "to",
        "of",
        "in",
        "on",
        "at",
        "for",
        "from",
        "by",
        "and",
        "or",
        "but",
        "with"
    }

    def tokenize(self, text):

        text = text.lower()

        text = re.sub(r"[^a-z0-9\s]", "", text)

        tokens = text.split()

        filtered = []

        for token in tokens:
            if token not in self.STOP_WORDS:
                filtered.append(token)

        return filtered