import torch
import torchvision
import torchvision.transforms as transforms 
import torchvision.datasets as datasets
import numpy as np
import torch.optim as optim
import torch.nn as nn
import pandas as pd
import os
import argparse
from PIL import Image
import matplotlib.pyplot as plt
import math
import torchvision.models as models
import timm
#torch.manual_seed(20)

def cv_forecast_image(filename, PATH ='./model/vision_model.pth'):
    weather_classes = [
    'dew', 'fogsmog', 'frost', 'glaze', 'hail', 'lightning','rain',
    'rainbow', 'rime', 'sandstorm', 'snow'
]

    model = models.vit_b_16(pretrained=True)
    model.heads.head = torch.nn.Linear(in_features=768, out_features=11)
    print("Head weights:", model.heads.head.weight[:5])


    state_dict = torch.load(PATH)
 

    # Load the modified state_dict into the model
    model.load_state_dict(state_dict, strict=False)
    model.eval()

    
    preprocess = transforms.Compose([
    transforms.Resize(224),  # Resize smaller images to 224x224
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    img = Image.open(filename)
    #img = Image.open('data/dataset/frost/3603.jpg')
    img_tensor = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
    _, predicted = torch.max(outputs, 1)

    predicted_class_name = weather_classes[predicted.item()]

    print('prediction result:', (f'{predicted_class_name}'))


    return predicted_class_name



def recommend_tool():
    pass

def recommend_clothing():
    pass

def adjust_forecast():
    pass

cv_forecast_image(filename = 'DemoImageSenior.jpg', PATH ='./model/vision_model.pth')