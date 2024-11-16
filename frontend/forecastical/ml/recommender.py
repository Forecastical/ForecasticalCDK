import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
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
'clothing':['jacket','jacket' 'raincoat','t-shirt', 'fleece','t-shirt','pants', 'shorts', 'jeans', 'scarf', 't-shirt', 'skirt'],
'gender':['male', 'female','male','male', 'male','female', 'male', 'female', 'female', 'male', 'female'],
'age':['adult','young adult','young adult','adult', 'young adult','young adult', 'young adult', 'teen', 'adult', 'elderly', 'adult'],
'weather': ['cold', 'cold', 'rainy', 'sunny', 'cold', 'sunny', 'rainy', 'cold', 'cold', 'sunny', 'sunny']

}

for key in data.keys(): print(key, len(data[key]))

class ClothingRecommender():

    def __init__(self, model, feedback)->None:
        self.model = model
        self.feedback = feedback
 
    def preprocess(self,X,y)->None:
        self.label_encoder = LabelEncoder()
        self.hot_encoder = OneHotEncoder()
    
        self.X_enc = self.hot_encoder.fit_transform(X)
        self.Y_enc = self.label_encoder.fit_transform(y)

    def train(self)->None:
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X_enc, self.Y_enc)
        self.model.fit(self.X_train,self.Y_train)


    def predict(self, k:int):
        predicted_probs = self.model.predict_proba(self.X_test)
        predicted_recommendations = np.argsort(predicted_probs, axis=1)[:,-k:]
        return predicted_recommendations
    
    def get_converted_features(self, recommendations):
        classes =  self.label_encoder.inverse_transform(recommendations[0])
        return classes
    
    def get_classes_ordered(self, classes, order='higest'):
        if order == 'highest':
            return reversed(classes)
        elif order == 'lowest':
            return classes

    def update_user_profile()->None:
        pass


    def get_recommendations()->None:
        pass

    def save_model(self)->None:
        os.makedirs('model', exist_ok=True)
        with open('./model/model.pkl', 'wb') as file:
            pickle.dump(self.model, file)
        print("Model generated.")

    def load_model(self, filename)->None:
        model = pickle.load(open(filename, 'rb'))
        return model

if __name__ == '__main__':
   df = pd.DataFrame(data)
   features = ['gender', 'age', 'weather']
   model = ClothingRecommender(model = RandomForestClassifier(), feedback = None)
   X = df.drop(columns=features)
   y = df['clothing']
   model.preprocess(X = X, y = y)
   model.train()
   recommendations = model.predict(k = 2)
   print(model.get_converted_features(recommendations))
   model.save_model()
   loaded_model = model.load_model(filename = './model/model.pkl')
   model.model = loaded_model
   print(model.get_converted_features(model.predict(k = 3)))


RandomForestClassifier


def update_user_profile()->None:
    pass


def get_recommendations()->None:
    pass

def save_model(model, filename = 'clothing_recommender')->None:
    with open('/path/to/save/random_forest_model.pkl', 'wb') as file:
        pickle.dump(model, filename)
    print("Model saved.")

def load_model(filename, model)->None:

    model = pickle.load(open(filename, 'rb'))
    return model
