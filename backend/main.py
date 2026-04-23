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
        patents = get_patents(query)[:50]

        texts = [p.get("abstract", "") for p in patents if p.get("abstract")]

        if not texts:
            return {
                "query": query,
                "patents": [],
                "count": len(patents),   # 🔥 加這行
                "keywords": {},
                "trend": {},
                "message": "No valid patent data"
            }

        keyword_scores = analyze_texts(texts)

        # 👉 Trend（安全）
        trend = dict(Counter(keyword_scores.keys()))

        return {
            "query": query,
            "patents": patents,
            "keywords": keyword_scores,
            "trend": trend
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/wordcloud")
def wordcloud():
    return FileResponse("output/wordcloud.png")


@app.get("/tfidf")
def tfidf_chart():
    return FileResponse("output/tfidf.png")
