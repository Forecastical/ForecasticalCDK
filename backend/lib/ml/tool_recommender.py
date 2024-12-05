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
#df = pd.read_csv('synthetic_tools_data.csv')

# preprocess data in csv 
def process_age(df):
    df.loc[df['Age'] < 18, 'Age Group'] = "teen"
    df.loc[df['Age'].between(18,24), 'Age Group'] = "young adult"
    df.loc[df['Age'].between(25, 75), 'Age Group'] = "adult"
    df.loc[df['Age'] > 75, 'Age Group'] = "elderly" 
    return df 

def process_temp(df):
    df.loc[df['Temperature'] < 40, 'Temp'] = "cold"
    df.loc[df['Temperature'].between(40,59), 'Temp'] = "mild"
    df.loc[df['Temperature'].between(60,79), 'Temp'] = "warm"
    df.loc[df['Temperature'] >= 80, 'Temp'] = "hot"
    return df

#process_age(df)
#process_temp(df)


class ToolsRecommender:

    def __init__(self, model=None) -> None:
        self.model = model
        self.label_encoder = LabelEncoder()
        self.hot_encoder = OneHotEncoder()  
        self.feature_names = None

    def preprocess(self, X, y) -> None:
        self.feature_names = list(X.columns)
        self.X_enc = self.hot_encoder.fit_transform(X).toarray()
        self.Y_enc = self.label_encoder.fit_transform(y)

        self.feature_categories = {
            feature: list(X[feature].unique()) 
            for feature in self.feature_names
        }

    def train(self) -> None:
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            self.X_enc, self.Y_enc
        )
        self.model.fit(self.X_train, self.Y_train)

    def predict(self, user_data:np.ndarray, k: int):
        user_data_enc = self.hot_encoder.transform([user_data]).toarray()
        
        predicted_probs = self.model.predict_proba(user_data_enc)

        predicted_recommendations = np.argsort(predicted_probs, axis=1)[:, -k:]
        
        return predicted_recommendations

    def get_converted_features(self, recommendations):
        classes = self.label_encoder.inverse_transform(recommendations[0])
        return classes

    def get_classes_ordered(self, classes, order="higest"):
        if order == "highest":
            return reversed(classes)
        elif order == "lowest":
            return classes

    def save_model(self, path="./model") -> None:
        """Save model and preprocessing objects"""
        os.makedirs(path, exist_ok=True)
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'hot_encoder': self.hot_encoder,
            'feature_names': self.feature_names,
            'feature_categories': self.feature_categories
        }
        with open(os.path.join(path, "tool_model.pkl"), "wb") as file:
            pickle.dump(model_data, file)
        print("Model and preprocessing objects saved successfully.")

    def load_model(self, filename) -> None:
        """Load model and preprocessing objects"""
        with open(filename, "rb") as file:
            model_data = pickle.load(file)
            
        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']
        self.hot_encoder = model_data['hot_encoder']
        self.feature_names = model_data['feature_names']
        self.feature_categories = model_data['feature_categories']
        
        return self

'''
if __name__ == "__main__":
    df = pd.DataFrame(df)
    features = ["Age Group", "Temp", "Condition"]
    target = "Tool"
    X = df[features]
    y = df[target] 
    model = ToolsRecommender(model=RandomForestClassifier())
    model.preprocess(X=X, y=y)
    model.train()
    
    ex = np.array(["teen", "warm", "sunny"])
    recommendations = model.predict(user_data = ex, k=2)
    print(model.get_converted_features(recommendations))
    
    model.save_model()
    loaded_model = ToolsRecommender().load_model(filename="./model/tool_model.pkl")
    recommendations = loaded_model.predict(user_data=ex, k=3)
    print("Recommendations:", loaded_model.get_converted_features(recommendations))
'''