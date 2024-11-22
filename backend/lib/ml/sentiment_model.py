"""
Sentiment Model for comments

test is IMBD dataset

"""



import torch

from transformers import pipeline



# example of comment param
comments = [
    "I hate this experience.",
    "I love this product!",
    "I hate this experience.",
    "It's okay, nothing special.",
    "I hate this experience.",
    "I hate this experience.",
    "I hate this experience."
]

def get_comments(pipeline_type = "sentiment-analysis",comments = comments):
    sentiment_pipeline = pipeline(pipeline_type)

    results = sentiment_pipeline(comments)
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

    for result in results:
        label = result['label']
        sentiment_counts[label] += 1

    overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)

    return overall_sentiment
#print(overall_sentiment)




"""
Albert or Roberta
"""