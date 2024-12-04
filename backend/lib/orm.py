# orm.py
from peewee import *
from datetime import datetime


db = PostgresqlDatabase(
    "postgres", host="postgres", port=5432, user="postgres", password="postgres"
)

"""DB objects"""


class Users(Model):
    # Existing fields
    username = CharField(unique=True)
    password = CharField()
    user_fname = CharField()
    user_lname = CharField()
    user_age = IntegerField()
    home_lat = FloatField()
    home_lon = FloatField()
    use_celsius = BooleanField()
    user_alerts = BooleanField()
    # New fields
    profile_image = CharField(null=True)
    bio = TextField(null=True)
    preferred_activities = TextField(null=True)
    favorite_weather = CharField(null=True)
    notification_email = CharField(null=True)
    theme_preference = CharField(null=True, default='dark')

    class Meta:
        database = db

    #


#


class Comments(Model):
    user_id = ForeignKeyField(Users)
    comment = TextField()
    time_stamp = DateTimeField()
    lat = DoubleField()
    lon = DoubleField()

    class Meta:
        database = db
        db_table = "Comments"


class Posts(Model):
    user_id = ForeignKeyField(Users)
    image_path = CharField()  # Path to stored image
    caption = TextField()
    created_at = DateTimeField(default=datetime.now)
    weather_prediction = CharField(null=True)
    latitude = DoubleField()
    longitude = DoubleField()

    class Meta:
        database = db
        db_table = "Posts"

# Connect to the database and create the tables
def init_db():
    db.connect()
    db.create_tables([Users])
    db.create_tables([Posts])
    db.create_tables([Comments])
    print("Created table")

def extract_db_comments():
    comments = []
    
    for instance in Comments.select().where(Comments.comment.is_null(False)):
        comments.append(instance.comment)

    return comments
