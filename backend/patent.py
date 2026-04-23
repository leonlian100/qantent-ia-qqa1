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
            "size": 10   # 🔥 小量，避免 crash
        }

        headers = {
            "Content-Type": "application/json"
        }

        res = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=5   # 🔥 防卡死
        )

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

        # 👉 如果 API 沒資料，用 fallback
        if not patents:
            return fallback(query)

        return patents

    except Exception as e:
        print("API error:", e)
        return fallback(query)


def fallback(query):
    return [
        {"title": f"{query} device", "abstract": f"{query} cutting system using motor"},
        {"title": f"{query} machine", "abstract": f"automatic {query} with sensor"},
        {"title": f"{query} tool", "abstract": f"{query} blade rotation control"}
    ]
