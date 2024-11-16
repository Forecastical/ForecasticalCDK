from fastapi import FastAPI, File, UploadFile, HTTPException, status
from model_inference import cv_forecast_image
import uuid
import pickle
import numpy as np
import pandas as pd
from pydantic import BaseModel 
from peewee import *



app = FastAPI()
IMAGEDIR = "images/"


db = PostgresqlDatabase('postgres', host='postgres', port=5432, user='postgres', password='postgres')
class User (Model):
   name=TextField()
   city=TextField(constraints=[SQL("DEFAULT 'Mumbai'")])
   age=IntegerField()
   class Meta:
      database=db
      db_table='User'

db.connect()
db.create_tables([User])
print("Created table")

@app.post("/upload/", status_code=status.HTTP_201_CREATED)
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="only jpg images"
        )

    file.filename = f"{uuid.uuid4()}.jpg"
    file_path = f"{IMAGEDIR}{file.filename}"
   
    # writing contents to file
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File image upload failed"
        )

    # predicting the weather based on image 
    try:
        prediction = cv_forecast_image(file_path, PATH='./model/vision_model.pth')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="image prediction failed"
        )

    return {"prediction": prediction, "filename": file.filename, "status_code": 200}

# clothing reccomender api call