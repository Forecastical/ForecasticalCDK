import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os


"""
content based filtering approach

hybrid filtering approach

KNN, matrix factorization algorithm
SVD,LightFM

TF-IDF will be chosen for now. One model with user profiles.

"""
# gender, age, height, weather

data = {
    "clothing": [
        "jacket",
        "jacket", 
        "t-shirt",
        "fleece",
        "t-shirt",
        "pants",
        "shorts",
        "jeans",
        "scarf",
        "t-shirt",
        "skirt",
    ],
    "gender": [
        "male",
        "female",
        "male",
        "male",
        "male",
        "female",
        "male",
        "female",
        "female",
        "male",
        "female",
    ],
    "age": [
        "adult",
        "young adult",
        "young adult",
        "adult",
        "young adult",
        "young adult",
        "young adult",
        "teen",
        "adult",
        "elderly",
        "adult",
    ],
    "weather": [
        "cold",
        "cold",
        "rainy",
        "sunny",
        "cold",
        "sunny",
        "rainy",
        "cold",
        "cold",
        "sunny",
        "sunny",
    ],
}

for key in data.keys():
    print(key, len(data[key]))


class ClothingRecommender:

    def __init__(self, model) -> None:
        self.model = model

    def preprocess(self, X, y) -> None:
        self.label_encoder = LabelEncoder()
        self.hot_encoder = OneHotEncoder()

        self.X_enc = self.hot_encoder.fit_transform(X).toarray()
        self.Y_enc = self.label_encoder.fit_transform(y)

    def train(self) -> None:
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            self.X_enc, self.Y_enc
        )
        self.model.fit(self.X_train, self.Y_train)

    def predict(self, user_data:np.ndarray, k: int):
        user_data_enc = self.hot_encoder.transform([user_data]).toarray()
        predicted_probs = self.model.predict_proba(user_data_enc)


        # print(predicted_probs)
        predicted_recommendations = np.argsort(predicted_probs, axis=1)[:, -k:]
        # print(predicted_recommendations)
        # print(self.label_encoder.inverse_transform(predicted_recommendations[0]))
        # print(self.model.classes_[predicted_recommendations[0]])
        return predicted_recommendations

    def get_converted_features(self, recommendations):
        classes = self.label_encoder.inverse_transform(recommendations[0])
        return classes

    def get_classes_ordered(self, classes, order="higest"):
        if order == "highest":
            return reversed(classes)
        elif order == "lowest":
            return classes

    def save_model(self) -> None:
        os.makedirs("model", exist_ok=True)
        with open("./model/clothing_model.pkl", "wb") as file:
            pickle.dump(self.model, file)
        print("Model generated.")

    def load_model(self, filename) -> None:
        model = pickle.load(open(filename, "rb"))
        return model


if __name__ == "__main__":
    df = pd.DataFrame(data)
    print(df)
    features = ["gender", "age", "weather"]
    target = "clothing"
    X = df[features]
    y = df[target]

    model = ClothingRecommender(model=RandomForestClassifier())
    
    model.preprocess(X=X, y=y)
    model.train()
    ex = np.array(["male", "adult", "sunny"])

    recommendations = model.predict(user_data = ex, k=2)
    print(model.get_converted_features(recommendations))
    model.save_model()
    loaded_model = model.load_model(filename="./model/clothing_model.pkl")
    model.model = loaded_model
    print(model.get_converted_features(model.predict(user_data = ex, k=3)))