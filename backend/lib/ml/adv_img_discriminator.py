"""
Generative model that prevents malicious or non-weather related images from being uploaded
"""
import torch
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
import torch.nn.functional as F
from .model_inference import cv_forecast_image

def check_image(image_filename, PATH='./model/vision_model.pth'):
    model = models.vit_b_16(pretrained=True)
    model.heads.head = torch.nn.Linear(in_features=768, out_features=11)

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

    img = Image.open(image_filename)
    img_tensor = preprocess(img).unsqueeze(0)

    entropy = 0

    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = F.softmax(outputs, dim=1)
        entropy = -torch.sum(probabilities * torch.log(probabilities + 1e-8), dim=1).item()

    predicted_class = cv_forecast_image(image_filename, PATH)
    return entropy > 0.5 and predicted_class != "weather"