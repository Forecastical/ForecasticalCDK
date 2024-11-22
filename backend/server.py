from fastapi import FastAPI, File, UploadFile, HTTPException, status
from lib.ml.model_inference import cv_forecast_image
from lib.ml.forecast_update import update_forecast
from lib.ml.clothing_recommender import ClothingRecommender, process_age
from lib.ml.adv_img_discriminator import check_image
from lib.ml.sentiment_model import get_comments
from lib.orm import Users, Comments, Posts, extract_db_comments
from lib.model import UserAuth, UserCreate, UserUpdate, CreateComment, EditComment
from peewee import IntegrityError
from sklearn.ensemble import RandomForestClassifier
from lib.weather_processor import WeatherDataProcessor, get_weather_recommendation
import uuid
import time 
import os
import pandas as pd

# import pickle
import numpy as np

# import pandas as pd
from datetime import datetime


app = FastAPI()
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


@app.post("/user/validate")
async def validate_user(auth: UserAuth):
    if is_valid_user(auth):
        return success_response("User validated", 200)
    else:
        raise HTTPException(status_code=403, detail="Invalid credentials")


"Update User here"


@app.patch("/user")
async def update_user(auth: UserAuth, user_data: UserUpdate):
    try:
        if not is_valid_user(auth):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        user = Users.get(Users.username == auth.username)
        # update fields
        data_dict = user_data.dict(exclude_unset=True).items()
        for key, values in data_dict:
            setattr(user, key, values)

        return success_response("User updated", 200)
    # user doesn't exist
    except Users.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    # internal server error
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="unable to update user",
        )


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


@app.post("/upload_image", status_code=status.HTTP_201_CREATED)
async def create_upload_file(auth: UserAuth, file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="only jpg images"
        )

    try:
        user = Users.get(Users.username == auth.username)
    except Users.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="can't find user"
            )
    
    # create filepath and save images here locally 
    file.filename = f"{uuid.uuid4()}.jpg"
    user_dir = f"{IMAGEDIR}/{user.id}"
    os.path.join(user_dir, file.filename)
    file_path = os.makedirs(user_dir, exist_ok=True)

    # writing contents to file
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File image upload failed",
        )
        
    # predicting the weather based on image
    try:
        # check if image is fake first 
        img_check = check_image(file_path, PATH="./model/disc/vision_model.pth")

        if img_check:
            print("image is fake, try again")
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File image upload failed",
        )

        else:
            prediction = cv_forecast_image(file_path, PATH="./model/vision_model.pth")
            update = update_forecast(time.time, np.array[0.1, prediction])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="image prediction failed",
        )

    return {"prediction": prediction, "forcast update": update,
            "filename": file.filename, "status_code": 201}


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