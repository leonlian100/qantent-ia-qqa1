from sklearn.feature_extraction.text import TfidfVectorizer
import os

def analyze_texts(texts):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=10
    )

    X = vectorizer.fit_transform(texts)
    keywords = vectorizer.get_feature_names_out()

    return keywords.tolist()
