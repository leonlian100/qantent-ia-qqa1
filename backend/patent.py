import requests

def get_patents(query):

    # 👉 簡單英文 fallback（避免中文查不到）
    if query == "削鉛筆機":
        query = "pencil sharpener"

    try:
        url = "https://api.lens.org/patent/search"

        payload = {
            "query": {
                "query_string": {
                    "query": query
                }
            },
            "size": 10   # 🔥 先小量（避免爆）
        }

        headers = {"Content-Type": "application/json"}

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
            if abstract:
                patents.append({
                    "title": item.get("title", ""),
                    "abstract": abstract
                })

        # 👉 沒資料就 fallback
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
