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

df = pd.read_csv('synthetic_clothing_data.csv')

# preprocess data in csv 
def process_age(df):
    df.loc[df['Age'] < 18, 'Age Group'] = "teen"
    df.loc[df['Age'].between(18,24), 'Age Group'] = "young adult"
    df.loc[df['Age'].between(25, 75), 'Age Group'] = "adult"
    df.loc[df['Age'] > 18, 'Age Group'] = "elderly" 
    return df 

def process_temp(df):
    df.loc[df['Temperature'] < 40, 'Temp'] = "cold"
    df.loc[df['Temperature'].between(40,59), 'Temp'] = "mild"
    df.loc[df['Temperature'].between(60,79), 'Temp'] = "warm"
    df.loc[df['Temperature'] >= 80, 'Temp'] = "hot"
    return df

process_age(df)
process_temp(df)


class ClothingRecommender:

    def __init__(self, model, feedback) -> None:
        self.model = model
        self.feedback = feedback

    def preprocess(self, X, y) -> None:
        self.label_encoder = LabelEncoder()
        self.hot_encoder = OneHotEncoder()

        self.X_enc = self.hot_encoder.fit_transform(X)
        self.Y_enc = self.label_encoder.fit_transform(y)

    def train(self) -> None:
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            self.X_enc, self.Y_enc
        )
        self.model.fit(self.X_train, self.Y_train)

    def predict(self, new_features, k: int):
        predicted_probs = self.model.predict_proba(new_features)
        predicted_recommendations = np.argsort(predicted_probs, axis=1)[:, -k:]
        return predicted_recommendations

    def get_converted_features(self, recommendations):
        classes = self.label_encoder.inverse_transform(recommendations[0])
        return classes

    def get_classes_ordered(self, classes, order="highest"):
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
    df = pd.DataFrame(df)
    features = ["Age", "Temperature"]
    model = ClothingRecommender(model=RandomForestClassifier(), feedback=None)
    X = df.drop(columns=features)
    print(X)
    
    y = df["Clothing"]
    model.preprocess(X=X, y=y)
    model.train()
    
    
    recommendations = model.predict(k=2)
    print(model.get_converted_features(recommendations))
    model.save_model()
   
    
    