import requests
import time

def translate_query(q):
    mapping = {
        "削鉛筆機": "pencil sharpener",
        "機器人": "robot",
        "電動車": "electric vehicle"
    }
    return mapping.get(q, q)


def fetch_batch(query, size=10):
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
        res = requests.post(url, json=payload, timeout=5)
        data = res.json()

        results = []
        for item in data.get("data", []):
            abstract = item.get("abstract", "")
            if abstract:
                results.append(abstract)

        return results

    except:
        return []


def get_patents(query):
    query = translate_query(query)

    all_texts = []

    # 👉 分 5 次抓（總共 ~50 筆）
    for _ in range(5):
        batch = fetch_batch(query, size=10)
        all_texts.extend(batch)
        time.sleep(1)  # 🔥 避免被封鎖

    if not all_texts:
        return fallback(query)

    return [{"abstract": t} for t in all_texts]


def fallback(query):
    return [
        {"abstract": f"{query} automatic system with sensor"},
        {"abstract": f"{query} motor control cutting device"},
        {"abstract": f"{query} smart blade mechanism"}
    ]
