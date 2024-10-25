import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd

example = np.array([
    [0.1, 'dog'], 
    [0.2, 'cat'],
    [0.3, 'cat'],
    [1.1, 'bird'],
    [1.2, 'whale'],
    [2.3, 'bird'], 
    [2.5, 'bird'],   
    [3.7, 'bird']  
], dtype=object)

def update_forecast(time_threshold, prediction_matrix, alpha = 0.5):
    encoder = LabelEncoder()
    encoder.fit(prediction_matrix[:,1])
    
    prediction_matrix[:,1] = encoder.fit_transform(prediction_matrix[:,1])
    enc_classes = np.unique(prediction_matrix[:,1])
    unenc_classes = encoder.classes_
    #print(prediction_matrix[:,1])
    #print(prediction_matrix)


    #only take those temporally relevant
    utilized_predictions = prediction_matrix[np.where(prediction_matrix[:,0] >= time_threshold), 1]
    utilized_predictions= utilized_predictions.flatten()
    utilized_times = prediction_matrix[np.where(prediction_matrix[:,0] >= time_threshold), 0]
    utilized_times= utilized_times.flatten()

    data_series = pd.Series(utilized_predictions)
    ewma = data_series.ewm(alpha=alpha, adjust=False).mean().iloc[-1]
    closest_class = unenc_classes[np.argmin(np.abs(enc_classes))]

    return ewma,closest_class


    #print("Last average in sequence:", ewma_alpha)



update_forecast(time_threshold = 0.3, prediction_matrix = example)
