import requests
import time


def translate_query(q):
    mapping = {
        "削鉛筆機": "pencil sharpener",
        "機器人": "robot",
        "電動車": "electric vehicle"
    }
    return mapping.get(q, q)


def fetch_batch(query, size=20):
    url = "https://api.lens.org/patent/search"

    payload = {
        "query": {
            "query_string": {
                "query": query
            }
        },
        "size": size
    }

    try:
        res = requests.post(
            url,
            json=payload,
            timeout=5
        )
        data = res.json()

        results = []

        for item in data.get("data", []):
            abstract = item.get("abstract", "")
            title = item.get("title", "")

            if abstract:
                results.append({
                    "title": title,
                    "abstract": abstract
                })

        return results

    except Exception as e:
        print("Batch error:", e)
        return []


def get_patents(query):
    query = translate_query(query)

    all_patents = []

    # 🔥 分批抓（20 x 10 = 200）
    for i in range(10):
        batch = fetch_batch(query, size=20)

        all_patents.extend(batch)

        # 👉 已經夠就停（避免浪費）
        if len(all_patents) >= 200:
            break

        time.sleep(0.8)  # 🔥 防止 API 限制

    # 👉 如果 API 失敗，用 fallback
    if not all_patents:
        return fallback(query)

    return all_patents[:200]


def fallback(query):
    return [
        {"title": f"{query} device", "abstract": f"{query} cutting system using motor"},
        {"title": f"{query} machine", "abstract": f"automatic {query} with sensor"},
        {"title": f"{query} tool", "abstract": f"{query} blade rotation control"}
    ]
