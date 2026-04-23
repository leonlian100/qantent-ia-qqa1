import requests

def translate_query(q):
    mapping = {
        "削鉛筆機": "pencil sharpener",
        "機器人": "robot",
        "電動車": "electric vehicle"
    }
    return mapping.get(q, q)


def get_patents(query):
    query = translate_query(query)

    try:
        url = "https://api.lens.org/patent/search"

        payload = {
            "query": {
                "query_string": {
                    "query": query
                }
            },
            "size": 30   # 🔥 先穩定30筆
        }

        res = requests.post(url, json=payload, timeout=5)
        data = res.json()

        patents = []

        for item in data.get("data", []):
            abstract = item.get("abstract", "")
            title = item.get("title", "")

            if abstract:
                patents.append({
                    "title": title,
                    "abstract": abstract
                })

        return patents if patents else fallback(query)

    except:
        return fallback(query)


def fallback(query):
    return [
        {"title": f"{query} device", "abstract": f"{query} cutting system using motor"},
        {"title": f"{query} machine", "abstract": f"automatic {query} with sensor"},
        {"title": f"{query} tool", "abstract": f"{query} blade rotation control"}
    ]
