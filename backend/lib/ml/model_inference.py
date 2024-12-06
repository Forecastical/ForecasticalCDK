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

# torch.manual_seed(20)


import torch
import torchvision.models as models
import os

def cv_forecast_image(filename, PATH="./model/vision_model.pth"):
    print(f"Loading vision model from path: {PATH}")
    
    try:
        weather_classes = [
            "dew", "fogsmog", "frost", "glaze", "hail",
            "lightning", "rain", "rainbow", "rime",
            "sandstorm", "snow"
        ]

        # First load the state dict to check its shape
        state_dict = torch.load(PATH, map_location=torch.device('cpu'))
        print("Loaded state dict")
        
        # Get the number of classes from the loaded model
        num_classes = state_dict['heads.head.weight'].shape[0]
        print(f"Number of classes in saved model: {num_classes}")

        # Initialize the model with the correct number of classes
        model = models.vit_b_16(pretrained=True)
        model.heads.head = torch.nn.Linear(in_features=768, out_features=num_classes)
        print(f"Modified model head to match saved model: {num_classes} classes")
        
        # Load the state dict
        model.load_state_dict(state_dict, strict=True)
        print("Loaded state dict into model")
        
        model.eval()

        preprocess = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        ])
        
        print(f"Opening image from: {filename}")
        img = Image.open(filename)
        img_tensor = preprocess(img).unsqueeze(0)

        with torch.no_grad():
            outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)

        # Make sure we don't go out of bounds of our classes list
        predicted_idx = min(predicted.item(), len(weather_classes) - 1)
        predicted_class_name = weather_classes[predicted_idx]
        print(f"Raw prediction index: {predicted.item()}")
        print(f"Adjusted prediction index: {predicted_idx}")
        print(f"Prediction result: {predicted_class_name}")

        return predicted_class_name

    except Exception as e:
        print(f"Error in cv_forecast_image: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in model directory: {os.listdir('./model') if os.path.exists('./model') else 'model dir not found'}")
        raise e


def recommend_tool():
    pass


def recommend_clothing():
    pass


def adjust_forecast():
    pass


# cv_forecast_image(filename = 'DemoImageSenior.jpg', PATH ='./model/vision_model.pth')
