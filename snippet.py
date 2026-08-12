import re


class SnippetGenerator:

    def generate(self, text, query, max_length=250):

        if not text:
            return "No preview available."

        text = " ".join(text.split())

        if not query:
            return text[:max_length]

        query_words = query.lower().split()

        positions = []

        for word in query_words:

            match = re.search(
                re.escape(word),
                text,
                re.IGNORECASE
            )

            if match:
                positions.append(match.start())

        # Query word wasn't found, so still return useful text
        if not positions:
            snippet = text[:max_length]

            if len(text) > max_length:
                snippet += " ..."

            return snippet

        center = min(positions)

        start = max(0, center - 100)
        end = min(len(text), start + max_length)

        snippet = text[start:end]

        if start > 0:
            snippet = "... " + snippet

        if end < len(text):
            snippet += " ..."

        return snippet