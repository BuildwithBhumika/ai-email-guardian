"""
model.py - Train and save the Naive Bayes email classifier

Run this file directly to (re)train the model:
  python model.py
"""

import os
import pickle
import csv
from preprocessing import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def load_dataset(csv_path):
    """Read training data from the CSV file."""
    texts, labels = [], []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row['text'].strip()
            label = row['label'].strip().lower()
            if text and label:
                texts.append(preprocess(text))
                labels.append(label)
    return texts, labels


def train_model(csv_path=None):
    """
    Train a TF-IDF + Naive Bayes pipeline on the dataset.
    Saves model.pkl and vectorizer.pkl in the same directory.
    """
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')

    print("Loading training data...")
    texts, labels = load_dataset(csv_path)
    print(f"  Loaded {len(texts)} samples")
    print(f"  Label breakdown: { {l: labels.count(l) for l in set(labels)} }")

    # Split into train/test so we can report accuracy
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # TF-IDF converts text to numeric feature vectors
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),   # capture single words and two-word phrases
        max_features=5000,
        min_df=1,
    )

    # Multinomial Naive Bayes works great for text classification
    classifier = MultinomialNB(alpha=0.5)

    X_train_vec = vectorizer.fit_transform(X_train)
    classifier.fit(X_train_vec, y_train)

    # Evaluate on held-out test set
    X_test_vec = vectorizer.transform(X_test)
    y_pred = classifier.predict(X_test_vec)
    print("\nModel performance on test set:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Save both the vectorizer and classifier separately
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, 'model.pkl')
    vectorizer_path = os.path.join(base_dir, 'vectorizer.pkl')

    with open(model_path, 'wb') as f:
        pickle.dump(classifier, f)
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)

    print(f"\nModel saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")
    return classifier, vectorizer


def load_model():
    """Load pre-trained model and vectorizer from disk."""
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, 'model.pkl')
    vectorizer_path = os.path.join(base_dir, 'vectorizer.pkl')

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("No saved model found. Training a new one...")
        return train_model()

    with open(model_path, 'rb') as f:
        classifier = pickle.load(f)
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)

    return classifier, vectorizer


def predict(text, classifier, vectorizer):
    """
    Classify a single email text.
    Returns (category, confidence, probabilities_dict).
    """
    from preprocessing import preprocess
    clean = preprocess(text)
    vec = vectorizer.transform([clean])
    proba = classifier.predict_proba(vec)[0]
    classes = classifier.classes_
    category = classes[proba.argmax()]
    confidence = float(proba.max())

    proba_dict = {cls: round(float(p), 4) for cls, p in zip(classes, proba)}
    return category, confidence, proba_dict


if __name__ == '__main__':
    train_model()
