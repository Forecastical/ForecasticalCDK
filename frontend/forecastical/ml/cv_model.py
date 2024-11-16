"""
Computer Vision model to analyze scene and classify the weather

"""


import torch
import torch.nn as nn
from torchvision import transforms, datasets
import torchvision.models as models
from torch.utils.data import DataLoader, random_split
import torch.optim as optim
import os
from sklearn.model_selection import train_test_split

transform = transforms.Compose([
    transforms.Resize((224, 224)),transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])
number_of_classes = None
dataset = datasets.ImageFolder(root='./data/dataset', transform=transform)


train_val_dataset, test_dataset = train_test_split(dataset, test_size=0.2)


train_dataset, val_dataset = train_test_split(train_val_dataset, test_size=0.125)


train_loader = DataLoader(train_dataset, batch_size=64, num_workers=0, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64, num_workers=0, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=64, num_workers=0, shuffle=False)

model = models.vit_b_16(pretrained=False)

model.load_state_dict(torch.load('./model/vit_b_16_pretrained.pth'))

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print(device)
criterion = nn.CrossEntropyLoss()

types_of_weather = 12

model.heads.head = torch.nn.Linear(model.heads.head.in_features, types_of_weather)
model = model.to(device)
for param in model.parameters():
    param.requires_grad = False

for param in model.heads.parameters():
    param.requires_grad = True


optimizer = optim.Adam(model.heads.parameters(), lr=0.001)
for epoch in range(5):
    correct = 0

    total = 0
    running_loss = 0



    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad() 

        outputs = model(images)  
        loss = criterion(outputs, labels)  

        loss.backward()  
        optimizer.step()  

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print(f"Epoch [{epoch+1}], Loss: {running_loss/total}, Acc: {correct/total}")


def test(model, loader):
    model.eval() 
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in loader:

            images, labels = images.to(device), labels.to(device)
            outputs = model(images)

            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    accuracy = correct / total
    return accuracy

def save(PATH='./model/vision_model.pth'):
    torch.save(model.state_dict(), PATH)
