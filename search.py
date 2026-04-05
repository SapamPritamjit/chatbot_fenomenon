from ddgs import DDGS

def search_web(query):
    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(f"Title: {r['title']}\nContent: {r['body']}\n")
    except:
        return "No real-time data available."

    return "\n".join(results)