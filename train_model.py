import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Paths
CSV_PATH = "spam.csv"
MODEL_PATH = "spam_model.pkl"
VECTORIZER_PATH = "count_vectorizer.pkl"

def train_and_export():
    # 1. Load and clean data
    df = pd.read_csv(CSV_PATH, encoding="latin-1")
    df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
    df = df.dropna(subset=['message', 'class'])
    df['label'] = df['class'].map({'ham': 0, 'spam': 1})

    # 2. Prepare features and labels
    X_text = df['message']
    y = df['label']

    if X_text.empty or y.empty:
        raise RuntimeError("No data available to train on.")

    # 3. Vectorize text
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_text)

    # 4. Train classifier
    clf = MultinomialNB()
    clf.fit(X, y)

    # 5. Export model and vectorizer
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"Training complete: model ({len(df)} samples),")
    print(f"  • Model saved to:       {MODEL_PATH}")
    print(f"  • Vectorizer saved to: {VECTORIZER_PATH}")

if __name__ == "__main__":
    train_and_export()
