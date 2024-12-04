import numpy as np
import pandas as pd

ages = range(1, 99)
temperatures = range(0, 100)
conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]

clothing_items = [
    "t-shirt", "sweater", "jacket", "shorts", "jeans", 
    "raincoat", "boots", "sneakers", "scarf", "hat", "gloves", "coat"
]

# Probabilistic rules
def get_clothing(age, temp, condition):
    probabilities = []
    
    if temp < 32:
        probabilities = [0.05, 0.2, 0.3, 0.0, 0.4, 0.1, 0.6, 0.1, 0.4, 0.4, 0.5, 0.7]
    elif (32 <= temp) and (temp < 50):
        probabilities = [0.1, 0.4, 0.4, 0.05, 0.4, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.3]
    elif (50 <= temp) and (temp < 65):
        probabilities = [0.3, 0.2, 0.2, 0.1, 0.4, 0.1, 0.05, 0.5, 0.05, 0.1, 0.0, 0.1]
    elif (65 <= temp) and (temp < 85):
        probabilities = [0.5, 0.1, 0.1, 0.3, 0.3, 0.1, 0.0, 0.6, 0.0, 0.1, 0.0, 0.0]
    else:
        probabilities = [0.7, 0.0, 0.0, 0.6, 0.1, 0.1, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0]
    
    if condition == "rainy":
        probabilities[5] += 0.6  # Raincoat
        probabilities[6] += 0.2  # Boots
    if condition == "snowy":
        probabilities[-1] += .3  # Coat
        probabilities[-2] += .3  # Gloves
        probabilities[-3] += .2  # Hat
        probabilities[6] += .3
    if condition == "windy":
        probabilities[8] += 0.2  # Scarf
        probabilities[5] += .1   # raincoat
    if condition == "sunny":
        probabilities[3] += 0.3  # Shorts
        probabilities[0] += .2   # t-shirt
    if condition == "cloudy":
        probabilities[1] += .2
        probabilities[2] += .2
        probabilities[4] += .3
    
    # Adjust probabilities based on age
    if age < 5:
        probabilities[9] += 0.2  # Hat
        probabilities[1] += .2   # sweater
        probabilities[6] += .3   # boots
    elif (5 <= age) and (age < 12): # (kids dont get cold)
        probabilities[-1] -=.1
        probabilities[-2] -=.1
        probabilities[-3] -=.1
        probabilities[-4] -=.1
        
    elif age > 60:  # make sure retirement age does not get pneumonia
        probabilities[4] += 0.2
        probabilities[-1] += .2
        probabilities[-2] += .2
        probabilities[-3] += .2
        probabilities[2] += .2
    

    probabilities = np.clip(np.array(probabilities), 0, 100)
    probabilities = probabilities / probabilities.sum()
    
    return np.random.choice(clothing_items, p=probabilities)

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
        clothing = get_clothing(age, temp, condition)
        data.append({"Age": age, "Temperature": temp, "Condition": condition, "Clothing": clothing})
    return pd.DataFrame(data)

# Generate and save data
synthetic_data = generate_data(1000)
synthetic_data.to_csv("synthetic_clothing_data.csv", index=False)
print(synthetic_data.head())
