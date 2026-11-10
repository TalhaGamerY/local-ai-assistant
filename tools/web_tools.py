from duckduckgo_search import DDGS


def get_current_news(query: str = "world news today", max_results: int = 5) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))

        if not results:
            return "No current news results found."

        formatted = []
        for item in results:
            title = item.get("title", "No title")
            source = item.get("source", "Unknown source")
            date = item.get("date", "Unknown date")
            body = item.get("body", "")
            url = item.get("url", "")

            formatted.append(
                f"Title: {title}\nSource: {source}\nDate: {date}\nSummary: {body}\nURL: {url}"
            )

        return "\n\n".join(formatted)

    except Exception as error:
        return f"News search failed: {error}"
