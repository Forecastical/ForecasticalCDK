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

'''DB objects'''
class Users (Model):
    '''need user_id here to asso user with unique id'''
    username = TextField()
    password = TextField()
    user_fname = TextField()
    user_lname = TextField()
    user_age = IntegerField()
    home_lat = DoubleField()
    home_lon = DoubleField()
    use_celsius = BooleanField()
    user_alerts = BooleanField() # Not sure what this does.
    class Meta:
        database=db
        db_table='Users'
    #
#

class Comments (Model):
    user_id = ForeignKeyField(Users)
    comment = TextField()
    time_stamp = DateTimeField()
    lat = DoubleField()
    lon = DoubleField()
    class Meta:
        database=db
        db_table='Comments'

class Posts (Model):
    user_id = ForeignKeyField(Users)
    #image = TextField() # Peewee does not support storing images in pgsql.
    # We can grab the image file from ./data/<username>/<post_id>.png
    caption = TextField()
    time_stamp = DateTimeField()
    lat = DoubleField()
    lon = DoubleField()
    class Meta:
        database=db
        db_table='Posts'

db.connect()
db.create_tables([Users])
db.create_tables([Posts])
db.create_tables([Comments])

print("Created table")

'''Pydantic models for Handling User Input'''
class UserCreate(BaseModel):
    username: str
    password: str
    user_fname: str
    user_lname: str
    user_age: int
    home_lat: float
    home_lon: float
    use_celsius: bool
    user_alerts: bool

## Users
# Register user
# Login as user ?? 

## Posts
# Create post
# Edit Post
# Delete post

## Comments
# Create Comment
# Edit comment
# Delete Comment

## Recommendations
# Get recommendations?

'''DB API Calls'''

# two API calls with Account class, 1 to create user and other to update user info

# create user with POST request
@app.post("/users/")
async def create_user(request = UserCreate):
    # create a user 
    try:
        new_user = Users(request.username, request.password, 
                         request.user_fname, request.user_fname, request.user_age,
                         request.home_lat, request.home_lon, request.use_celsius, 
                         request.user_alerts)
        
        return {"new user created": new_user.username, "status_code": 201}
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to create user"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred"
        )
        




'''AI/ML API Calls'''
@app.post("/upload_image/", status_code=status.HTTP_201_CREATED)
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

    return {"prediction": prediction, "filename": file.filename, "status_code": 201}

# clothing reccomender api call
