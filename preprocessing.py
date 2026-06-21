"""
preprocessing.py - Text cleaning and tokenization for email analysis
"""

import re
import string

# Common English stopwords we want to remove
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "dare",
    "ought", "used", "i", "me", "my", "myself", "we", "our", "ours",
    "ourselves", "you", "your", "yours", "yourself", "yourselves", "he",
    "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
    "itself", "they", "them", "their", "theirs", "themselves", "what",
    "which", "who", "whom", "this", "that", "these", "those", "am", "s",
    "about", "above", "after", "again", "against", "all", "any", "because",
    "before", "between", "both", "each", "few", "further", "here", "how",
    "if", "into", "more", "most", "no", "not", "now", "only", "other",
    "out", "over", "own", "same", "so", "some", "such", "than", "then",
    "there", "through", "too", "under", "until", "up", "very", "while",
    "just", "please", "also", "get", "us", "as", "when", "where",
}


def preprocess(text):
    """
    Clean and tokenize email text for classification.
    Returns a single string of clean, space-joined tokens.
    """
    # Step 1: Make everything lowercase so capitalization doesn't matter
    text = text.lower()

    # Step 2: Keep URLs as a token but simplify them
    text = re.sub(r'https?://\S+', ' urllink ', text)

    # Step 3: Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Step 4: Split into individual words
    tokens = text.split()

    # Step 5: Remove stopwords and short words (less than 2 characters)
    tokens = [
        word for word in tokens
        if word not in STOPWORDS and len(word) > 2
    ]

    return ' '.join(tokens)
