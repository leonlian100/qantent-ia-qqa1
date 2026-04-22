from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import os

STOPWORDS_EXTRA = [
    "method", "device", "system", "apparatus",
    "said", "comprising", "includes"
]

def analyze_texts(texts):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=20
    )

    X = vectorizer.fit_transform(texts)
    keywords = vectorizer.get_feature_names_out()

    os.makedirs("output", exist_ok=True)

    wc = WordCloud(
        width=800,
        height=400,
        stopwords=set(STOPWORDS_EXTRA)
    ).generate(" ".join(texts))

    wc.to_file("output/wordcloud.png")

    return keywords.tolist()
