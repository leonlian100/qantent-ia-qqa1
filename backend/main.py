from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from patent import get_patents
from nlp import analyze_texts

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
    query = data.get("text", "")

    patents = get_patents(query)[:50]

    texts = [p["abstract"] for p in patents]

    keywords = analyze_texts(texts)

    return {
        "query": query,
        "patents": patents,
        "keywords": keywords
    }

@app.get("/wordcloud")
def wordcloud():
    return FileResponse("output/wordcloud.png")

@app.get("/tfidf")
def tfidf_chart():
    return FileResponse("output/tfidf.png")
