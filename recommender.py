import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

"""
content based filtering approach

hybrid filtering approach

KNN, matrix factorization algorithm
SVD,LightFM

TF-IDF will be chosen for now. One model with user profiles.

"""

class ClothingRecommender:

    def __init__(self, user_profiles, feedback):
        self.user_profiles = user_profiles
        self.feedback = feedback
        pass

df = data

vectorizer = TfidfVectorizer()


matrix = vectorizer.fit_transform(df['features'])

cos_sim = cosine_similarity(matrix, matrix)


def update_user_profile()->None:
    pass


def get_recommendations()->None:
    pass

def save_model(filename = 'recommender')->None:
    model = {'vectorizer':vectorizer, 'matrix':matrix, 'profiles':user_profiles}
    pickle.dump(model, open(filename, 'wb'))
    print("Model saved.")
    

    




