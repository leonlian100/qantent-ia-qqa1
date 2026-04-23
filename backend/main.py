from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from patent import get_patents
from nlp import analyze_texts
from collections import Counter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate(data: dict):
    query = data.get("text", "").strip()

    if not query:
        return {"error": "No input text provided"}

    try:
        # 👉 抓專利（最多50筆）
        patents = get_patents(query)[:50]

        # 👉 防止空資料 crash
        texts = [p.get("abstract", "") for p in patents if p.get("abstract")]

        if not texts:
            return {
                "query": query,
                "patents": [],
                "keywords": {},
                "trend": {},
                "message": "No valid patent data"
            }

        # 👉 NLP 分析（你原本穩定版本）
        keyword_scores = analyze_texts(texts)

        # 👉 Trend（安全加，不動 nlp）
        trend = dict(Counter(keyword_scores.keys()))

        return {
            "query": query,
            "patents": patents,
            "keywords": keyword_scores,
            "trend": trend
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.get("/wordcloud")
def wordcloud():
    return FileResponse("output/wordcloud.png")


@app.get("/tfidf")
def tfidf_chart():
    return FileResponse("output/tfidf.png")
