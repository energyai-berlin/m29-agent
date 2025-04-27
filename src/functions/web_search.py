import requests

def web_search(query, num_results=5):
    """
    Perform a web search using DuckDuckGo Instant Answer API.

    Args:
        query (str): The search query.
        num_results (int): Number of results to return.

    Returns:
        list: A list of dictionaries with 'title', 'url', and 'snippet'.
    """
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1,
        "skip_disambig": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    # Parse related topics for results
    for topic in data.get("RelatedTopics", []):
        if "Text" in topic and "FirstURL" in topic:
            results.append({
                "title": topic.get("Text"),
                "url": topic.get("FirstURL"),
                "snippet": topic.get("Text")
            })
        # Sometimes topics are nested
        elif "Topics" in topic:
            for subtopic in topic["Topics"]:
                if "Text" in subtopic and "FirstURL" in subtopic:
                    results.append({
                        "title": subtopic.get("Text"),
                        "url": subtopic.get("FirstURL"),
                        "snippet": subtopic.get("Text")
                    })
        if len(results) >= num_results:
            break

    return results[:num_results]