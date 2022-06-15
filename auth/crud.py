from utils.dbUtil import database
from schemas import schemas


def find_exist_user(email : str):
    query = "select * from py_users where status='1' and email=:email"
    return database.fetch_one(query , values={"email": email})

def save_user(user: schemas.UserCreate):
    query = "INSERT INTO py_users VALUES(nextval('user_id_seq'), :email, :password , :fullname, now() at time zone 'UTC','1' ) "
    return database.execute(query , values = {"email": user.email , "password": user.password , "fullname" : user.fullname  })