from model_inference import cv_forecast_image
import os

def test_model():
    # List of test images
    test_images = [
        'DemoImageSenior.jpg',
        # add more test images here
    ]
    
    for image in test_images:
        if os.path.exists(image):
            try:
                result = cv_forecast_image(image)
                print(f"Image: {image}, Prediction: {result}")
            except Exception as e:
                print(f"Error processing {image}: {str(e)}")
        else:
            print(f"Image {image} not found")

if __name__ == "__main__":
    test_model()
