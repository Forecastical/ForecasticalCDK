from fastapi import FastAPI, File, UploadFile, HTTPException, status, Query, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from lib.ml.model_inference import cv_forecast_image
from lib.ml.forecast_update import update_forecast
from lib.ml.clothing_recommender import ClothingRecommender, process_age
from lib.ml.adv_img_discriminator import check_image
from lib.ml.sentiment_model import get_comments
from lib.orm import Users, Comments, Posts, extract_db_comments, init_db
from lib.model import UserAuth, UserCreate, UserUpdate, CreateComment, EditComment
from peewee import IntegrityError
from sklearn.ensemble import RandomForestClassifier
from lib.weather_processor import WeatherDataProcessor, get_weather_recommendation
import uuid
import time 
import os
import pandas as pd
import json


# import pickle
import numpy as np

# import pandas as pd
from datetime import datetime

IMAGEDIR = "./data"
PROFILE_IMAGES_DIR = os.path.join(IMAGEDIR, "profile_images")
WEATHER_IMAGES_DIR = os.path.join(IMAGEDIR, "weather_images/posts")

os.makedirs(PROFILE_IMAGES_DIR, exist_ok=True)
os.makedirs(WEATHER_IMAGES_DIR, exist_ok=True)


app = FastAPI()
app.mount("/data", StaticFiles(directory="data"), name="data")

# Add CORS middleware configuration right after creating the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",  # Your frontend dev server
        "http://localhost:8080",  # Common Vue dev server port
        "http://localhost:3000"   # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.mount("/data", StaticFiles(directory="data"), name="data")

IMAGEDIR = "./data/"
init_db()


def success_response(message, status_code):
    return {"message": message, "status_code": status_code}


def is_valid_user(auth: UserAuth):
    try:
        user = Users.get(Users.username == auth.username)
        return user.password == auth.password
    except Users.DoesNotExist:
        return False


"Create New User here"


@app.post("/user")
async def create_user(request: UserCreate):
    # create a user
    try:
        new_user = Users.create(
            username=request.username,
            password=request.password,
            user_fname=request.user_fname,
            user_lname=request.user_lname,
            user_age=request.user_age,
            home_lat=request.home_lat,
            home_lon=request.home_lon,
            use_celsius=request.use_celsius,
            user_alerts=request.user_alerts,
        )

        return success_response("User created", 201)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred")


@app.options("/user/validate")
async def validate_user_options():
    return {"message": "OK"}

@app.post("/user/validate")
async def validate_user(auth: UserAuth):
    print(f"Received login request for user: {auth.username}")  # Debug log
    try:
        if is_valid_user(auth):
            print("User validation successful")  # Debug log
            user = Users.get(Users.username == auth.username)
            return {
                "message": "User validated",
                "status_code": 200,
                "username": user.username,
                "password": user.password,  # Be careful with this in production
                "user_fname": user.user_fname,
                "user_lname": user.user_lname,
                "user_age": user.user_age,
                "home_lat": user.home_lat,
                "home_lon": user.home_lon,
                "use_celsius": user.use_celsius,
                "user_alerts": user.user_alerts
            }
        else:
            print("User validation failed")  # Debug log
            raise HTTPException(status_code=403, detail="Invalid credentials")
    except Exception as e:
        print(f"Error during validation: {str(e)}")  # Debug log
        raise

"Update User here"

@app.post("/user/profile-image")
async def upload_profile_image(auth: UserAuth, file: UploadFile = File(...)):
    try:
        if not is_valid_user(auth):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        # Validate image file
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files allowed")

        # Create unique filename
        filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        file_path = os.path.join(PROFILE_IMAGES_DIR, filename)

        # Save file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # Update user profile in database
        user = Users.get(Users.username == auth.username)
        
        # Delete old profile image if exists
        if user.profile_image:
            old_file_path = os.path.join(PROFILE_IMAGES_DIR, user.profile_image)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        user.profile_image = filename
        user.save()

        return success_response("Profile image updated", 201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/user")
async def update_user(auth: UserAuth, user_data: UserUpdate):
    try:
        if not is_valid_user(auth):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        user = Users.get(Users.username == auth.username)
        
        # Convert the update data to dict and exclude None values
        update_data = user_data.dict(exclude_unset=True)
        
        # Update fields
        for key, value in update_data.items():
            setattr(user, key, value)
        
        user.save()
        
        # Return the complete updated user data
        return {
            "message": "User updated successfully",
            "status_code": 200,
            "username": user.username,
            "password": user.password,  # Be careful with this in production
            "user_fname": user.user_fname,
            "user_lname": user.user_lname,
            "user_age": user.user_age,
            "home_lat": user.home_lat,
            "home_lon": user.home_lon,
            "use_celsius": user.use_celsius,
            "user_alerts": user.user_alerts
        }

    except Users.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"Create comment here"


@app.post("/comment")
async def create_comment(auth: UserAuth, comment: CreateComment):
    try:
        if not is_valid_user(auth):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        new_comment = Comments(
            comment.user_id,
            comment.comment,
            datetime.datetime.now(),
            comment.lon,
            comment.lat,
        )

        return success_response(f"Comment created {new_comment.comment}", 201)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Failed to create comment")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred")


"Update Comment here"


@app.patch("/comment/{comment_id}")
async def update_comment(comment_id: int, auth: UserAuth, comment: EditComment):
    try:

        if (
            not is_valid_user(auth)
            or not Comments.get_by_id(comment_id).user_id
            == Users.get(username=auth.username).id
        ):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        # access the target comment
        edit_comment = Comments.get(Comments.id == comment_id)
        # get a dictionary of the new comment data
        data_dict = comment.dict(exclude_unset=True).items()
        # update the comment
        for key, value in data_dict:
            setattr(edit_comment, key, value)

        return success_response("Comment updated", 200)

    except Comments.DoesNotExist:
        raise HTTPException(status_code=404, detail="comment not found")
    # internal server error
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="unable to update comment",
        )


"Delete comment here"


@app.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int, auth: UserAuth):
    try:
        if not is_valid_user(auth):
            raise HTTPException(status_code=403, detail="Invalid credentials")
        # Get the comment
        comment = Comments.get_by_id(comment_id)
        # Get the author of the comment
        author = Users.get(Users.username == auth.username)
        # Check if the auth is for the comment author
        if not auth.username == author.username:
            raise HTTPException(status_code=403, detail="Invalid credentials")
        # delete comment
        comment.delete_instance()
        return success_response("Comment deleted", 200)

    except Comments.DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred")


"""AI/ML API Calls"""


# clothing reccomender api call
@app.get("/clothes_reccomended", status_code=status.HTTP_200_OK)
async def reccomend_clothes(auth: UserAuth):
    users = Users.get(Users.username == auth.username)
    
    
    weather_recc = get_weather_recommendation(users.home_lat, users.home_lon)
    filtered_data = {
        'Temp': weather_recc['temperature_category'],
        'Condition': weather_recc['condition'],
        'Age Group': users.age
    }
    # check if the "target" col needs to be included
    df = pd.DataFrame.from_dict(filtered_data)
    process_age(df)

    try:
        model = ClothingRecommender(model=RandomForestClassifier(), feedback=None)
        loaded_model = model.load_model(filename=".lib/ml/model/clothing_model.pkl")
        model.model = loaded_model
        reccomendation = str(model.get_converted_features(model.predict(df, k=3)))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="clothes rec failed internally",
        )

    return {"prediction": reccomendation, "status_code": 200}

# tools reccomender API call 
@app.get("/tools_reccomended", status_code=status.HTTP_200_OK)
async def reccomend_tools(auth: UserAuth):
    users = Users.get(Users.username == auth.username)
    
    
    weather_recc = get_weather_recommendation(users.home_lat, users.home_lon)
    filtered_data = {
        'Temp': weather_recc['temperature_category'],
        'Condition': weather_recc['condition'],
        'Age Group': users.age
    }
    # check if the "target" col needs to be included
    df = pd.DataFrame.from_dict(filtered_data)
    process_age(df)

    try:
        model = ClothingRecommender(model=RandomForestClassifier(), feedback=None)
        loaded_model = model.load_model(filename=".lib/ml/model/tool_model.pkl")
        model.model = loaded_model
        reccomendation = str(model.get_converted_features(model.predict(df, k=3)))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="clothes rec failed internally",
        )

    return {"prediction": reccomendation, "status_code": 200}

@app.get("/activities_reccomended", status_code=status.HTTP_200_OK)
async def reccomend_tools(auth: UserAuth):
    users = Users.get(Users.username == auth.username)
    
    weather_recc = get_weather_recommendation(users.home_lat, users.home_lon)
    filtered_data = {
        'Temp': weather_recc['temperature_category'],
        'Condition': weather_recc['condition'],
        'Age Group': users.age
    }
    # check if the "target" col needs to be included
    df = pd.DataFrame.from_dict(filtered_data)
    process_age(df)

    try:
        model = ClothingRecommender(model=RandomForestClassifier(), feedback=None)
        loaded_model = model.load_model(filename=".lib/ml/model/activities_model.pkl")
        model.model = loaded_model
        reccomendation = str(model.get_converted_features(model.predict(df, k=3)))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="clothes rec failed internally",
        )

    return {"prediction": reccomendation, "status_code": 200}

# sentiment api call
@app.get("/sentiment", status_code=status.HTTP_200_OK)
async def sentiment():
    sentiment_comments = extract_db_comments()

    try:
        sentiment = get_comments(pipeline_type="sentiment-analysis", 
                                 comments=extract_db_comments)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="clothes rec failed internally",
        )
     
    return {"sentiment": sentiment, "status_code": 200}


@app.get("/feed_images")
async def get_feed_images(username: str = Query(...), password: str = Query(...)):
    try:
        auth = UserAuth(username=username, password=password)
        if not is_valid_user(auth):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        posts = []
        for post in Posts.select().order_by(Posts.created_at.desc()):
            user = Users.get_by_id(post.user_id)
            posts.append({
                "id": post.id,
                "url": f"/data/{post.image_path}",
                "caption": post.caption,
                "username": user.username,
                "location": f"{post.latitude}, {post.longitude}",
                "created_at": post.created_at.isoformat(),
                "weather_prediction": post.weather_prediction
            })
        
        return {"images": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/upload_image")
async def create_upload_file(file: UploadFile = File(...), caption: str = Form(...), auth: str = Form(...)):
    print(f"Received upload request - File: {file.filename}, Caption: {caption}")
    
    auth_data = json.loads(auth)
    auth_model = UserAuth(**auth_data)

    if not is_valid_user(auth_model):
        raise HTTPException(status_code=403, detail="Invalid credentials")

    try:
        user = Users.get(Users.username == auth_model.username)
        
        # Create unique filename and save path
        filename = f"{uuid.uuid4()}.jpg"
        post_dir = os.path.join(WEATHER_IMAGES_DIR, str(user.id))
        os.makedirs(post_dir, exist_ok=True)
        file_path = os.path.join(post_dir, filename)

        print(f"Saving file to: {file_path}")

        # Save file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # Create post record
        relative_path = f"weather_images/posts/{user.id}/{filename}"
        post = Posts.create(
            user_id=user.id,
            image_path=relative_path,
            caption=caption,
            created_at=datetime.now(),
            weather_prediction=None,
            latitude=user.home_lat,
            longitude=user.home_lon
        )

        print(f"Created post with ID: {post.id}")
        return {
            "message": "Image uploaded successfully",
            "post_id": post.id,
            "image_path": relative_path
        }

    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))