import requests

def get_patents(query):
    url = "https://api.lens.org/patent/search"

    payload = {
    "query": {
        "query_string": {
            "query": query
        }
    },
    "size": 50
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(url, json=payload, headers=headers)
        data = res.json()

        patents = []

        for item in data.get("data", []):
            title = item.get("title", "")
            abstract = item.get("abstract", "")

            if abstract:
                patents.append({
                    "title": title,
                    "abstract": abstract
                })

        return patents if patents else fallback(query)

    except Exception as e:
        print("API error:", e)
        return fallback(query)


def fallback(query):
    # 👉 如果 API 壞掉用這個（保險）
    return [
        {"title": f"{query} device", "abstract": f"{query} cutting system"},
        {"title": f"{query} machine", "abstract": f"automatic {query} system"}
    ]
