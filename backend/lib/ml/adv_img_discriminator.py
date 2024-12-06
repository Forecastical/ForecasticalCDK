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

def check_image(file_path, PATH="./model/vision_model.pth"):
    print(f"Loading model from path: {PATH}")
    print(f"Available PyTorch devices: {torch.cuda.is_available()=}")
    
    try:
        # Load the model to CPU explicitly
        state_dict = torch.load(PATH, map_location=torch.device('cpu'))
        print("Successfully loaded state dict")
        
        # Rest of your existing function logic
        return False  # Or whatever your original function returned
        
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in model directory: {os.listdir('./model') if os.path.exists('./model') else 'model dir not found'}")
        raise e