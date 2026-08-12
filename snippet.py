import re


class SnippetGenerator:

    def generate(self, text, query, max_length=250):

        text = " ".join(text.split())
        query = query.strip()

        if not text:
            return ""

        if not query:
            return text[:max_length]

        # Find the first occurrence of the query
        match = re.search(
            re.escape(query),
            text,
            re.IGNORECASE
        )

        if not match:
            return text[:max_length]

        start = max(0, match.start() - 100)
        end = min(len(text), match.end() + 150)

        snippet = text[start:end]

        if start > 0:
            snippet = "... " + snippet

        if end < len(text):
            snippet += " ..."

        return snippet