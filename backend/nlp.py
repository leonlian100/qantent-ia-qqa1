from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from collections import Counter

def keyword_trend(keywords):
    return Counter(keywords)
    
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
    scores = X.sum(axis=0).A1

    keyword_scores = dict(zip(keywords, scores))

    os.makedirs("output", exist_ok=True)

    # ✅ 文字雲
    wc = WordCloud(width=800, height=400).generate(" ".join(texts))
    wc.to_file("output/wordcloud.png")

    # ✅ TF-IDF 長條圖
    plt.figure()
    plt.bar(keyword_scores.keys(), keyword_scores.values())
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/tfidf.png")
    plt.close()

    return keyword_scores
