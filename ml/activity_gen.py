import numpy as np
import pandas as pd

ages = range(1, 99)
temperatures = range(0, 100)
conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]

activity_suggestions = [
   'hike','read', 'play board games','run', 'garden','picnic','swim', 'fly kites'

]

# Probabilistic rules
def get_clothing(age, temp, condition):
    probabilities = []
    
    if temp < 32:
        probabilities = [0.05, 0.3, 0.3, 0.05, 0.0, 0.0, 0.0, 0.1]
    elif (32 <= temp) and (temp < 50):
        probabilities = [0.1, 0.2, 0.2, 0.1, 0.05, 0.1, 0.0, 0.2]
    elif (50 <= temp) and (temp < 65):
        probabilities = [0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.05, 0.2]
    elif (65 <= temp) and (temp < 85):
        probabilities = [0.4, 0.1, 0.1, 0.3, 0.2, 0.5, 0.1, 0.2]
    else:
        probabilities = [0.5, 0.2, 0.2, 0.2, 0.4, 0.3, 0.5, 0.2]
    
    if condition == "rainy":
        probabilities[1] += 0.6
        probabilities[2] += 0.4
        probabilities[3] += .3
    if condition == "snowy":
        probabilities[1] += .2
        probabilities[2] += .3
    if condition == "windy":
        probabilities[-1] += .4  
    if condition == "sunny":
        probabilities[0] += .2
        probabilities[3] += .1
        probabilities[4] += .2
        probabilities[5] += .1
        if temp >= 60:
            probabilities[6] += .2
    
    if age < 5:
        probabilities[0] = 0  
        probabilities[3] = 0
        probabilities[2] += .4   
        probabilities[5] += .2   
        probabilities[6] += .1
        probabilities[7] += .1
    elif (5 <= age) and (age < 12): 
        probabilities[0] +=.4
        probabilities[2] +=.2
        probabilities[-2] +=.2
        
    elif age > 60:
        probabilities[3] = 0
        probabilities[1] += .2
        probabilities[2] += .2
        if temp >= 60 and condition not in ["rainy", "snowy"]:
            probabilities[4] += .5
    

    probabilities = np.clip(np.array(probabilities), 0, 100)
    probabilities = probabilities / probabilities.sum()
    
    return np.random.choice(activity_suggestions, p=probabilities)

def get_cond(temp):
    prob = []
    if temp < 32:
        prob = [.3, .3, .05, .5, .3]
    elif temp < 50:
        prob = [.2, .4, .3, .05, .4]
    elif temp < 65:
        prob = [.3, .3, .2, .0, .3]
    elif temp < 85:
        prob = [.5, .2, .2, .0, .2]
    else:
        prob = [.6, .2, .2, .0, .1]

    prob = np.array(prob)
    prob /= sum(prob)
    
    return np.random.choice(conditions, p=prob)

def generate_data(num_samples=10000):
    data = []
    for _ in range(num_samples):
        temp = int(np.clip(np.random.normal(50, 25), 0, 100))
        age = np.random.choice(ages)
 
        condition = get_cond(temp)
        activities = get_clothing(age, temp, condition)
        data.append({"Age": age, "Temperature": temp, "Condition": condition, "Activity": activities})
    return pd.DataFrame(data)

# Generate and save data
synthetic_data = generate_data(1000)
synthetic_data.to_csv("synthetic_activities_data.csv", index=False)
print(synthetic_data.head())


