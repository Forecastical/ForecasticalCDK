from peewee import *

db = PostgresqlDatabase(
    "postgres", host="postgres", port=5432, user="postgres", password="postgres"
)

"""DB objects"""


class Users(Model):
    """need user_id here to asso user with unique id"""

    username = TextField(unique=True)
    password = TextField()
    user_fname = TextField()
    user_lname = TextField()
    user_age = IntegerField()
    home_lat = DoubleField()
    home_lon = DoubleField()
    use_celsius = BooleanField()
    user_alerts = BooleanField()  # Not sure what this does.

    class Meta:
        database = db
        db_table = "Users"

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
    # image = TextField() # Peewee does not support storing images in pgsql.
    # We can grab the image file from ./data/<username>/<post_id>.png
    caption = TextField()
    time_stamp = DateTimeField()
    lat = DoubleField()
    lon = DoubleField()

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
