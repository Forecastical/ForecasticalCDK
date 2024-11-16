import torch

from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
from torchvision.models import ViT_B_16_Weights, vit_b_16

from PIL import Image

import os

def cv_forecast_image(filename, PATH='./model/vision_model.pth'):
    weather_classes = [
        'dew', 'fogsmog', 'frost', 'glaze', 'hail', 'lightning', 'rain',
        'rainbow', 'rime', 'sandstorm', 'snow'
    ]

    # Initialize model with pretrained weights
    model = vit_b_16(weights=ViT_B_16_Weights.DEFAULT)
    model.heads.head = nn.Linear(in_features=768, out_features=11)
    
    # Only try to load custom weights if the file exists
    if os.path.exists(PATH):
        print(f"Loading custom model from {PATH}")
        state_dict = torch.load(PATH)
        model.load_state_dict(state_dict, strict=False)
    else:
        print(f"Warning: Custom model file {PATH} not found. Using base pretrained model.")
    
    model.eval()
    
    preprocess = Compose([
        Resize(224),
        CenterCrop(224),
        ToTensor(),
        Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    
    # Verify image file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Image file {filename} not found")
        
    img = Image.open(filename)
    img_tensor = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
    _, predicted = torch.max(outputs, 1)

    predicted_class_name = weather_classes[predicted.item()]
    print('Prediction result:', predicted_class_name)

    return predicted_class_name

# Only run this if script is run directly
if __name__ == "__main__":
    # Test the function with a sample image
    test_image = "DemoImageSenior.jpg"
    if os.path.exists(test_image):
        result = cv_forecast_image(test_image)
        print(f"Test prediction: {result}")
    else:
        print(f"Test image {test_image} not found")
        