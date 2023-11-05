from typing import Union
from fastapi import FastAPI, HTTPException, Request 
from pydantic import BaseModel
import numpy as np
import base64
import cv2
import bcrypt
import mysql.connector #https://www.w3schools.com/python/python_mysql_update.asp
import datetime

app = FastAPI()

mydb = mysql.connector.connect(
    host="202.28.34.197",
    user="web65_64011212185",
    password="64011212185@csmsu",
    database="web65_64011212185"
)
mycursor = mydb.cursor()

class Item(BaseModel):
    image_base64 : str

class User(BaseModel):
    name : str
    email : str
    password : str
    photo : str

class LogIn(BaseModel):
    name_or_email : str
    password : str

class User_Image(BaseModel):
    name : str
    base64 : str
    UID : int

def readb64(uri):
   encoded_data = uri.split(',')[1] 
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)  
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

@app.get("/")
async def read_root():
    return {"Hello": "Hello World !!!"}


@app.post("/user")
async def insert_user(user : User):
    sql = "SELECT * FROM User WHERE email = %s"
    mycursor.execute(sql, (user.email,))
    myresult = mycursor.fetchall()
    if myresult:
        raise HTTPException(status_code=401, detail="Email already exists")
    else:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode(), salt) 
        user.password = hashed_password
        photo_base64 = user.photo.split(',')[1]
        user.photo = photo_base64

        sql = "INSERT INTO User (name, email, password, photo) VALUES (%s, %s, %s, %s)"
        val = (user.name, user.email, user.password, user.photo)
        mycursor.execute(sql, val)
        mydb.commit()
        return {"1 record inserted, ID:": mycursor.lastrowid}
    
@app.post("/user/LogIn")
async def user_LogIn(logIn : LogIn):
    sql = "SELECT * FROM User WHERE name = %s OR email = %s"
    val = (logIn.name_or_email, logIn.name_or_email)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if myresult:
        UID = myresult[0][0]
        if bcrypt.checkpw(logIn.password.encode(), myresult[0][3].encode()):
            sql = "SELECT User.UID, User.name, User.email, User.password, User.photo, COUNT(Friend.UID) AS friend_count FROM User LEFT JOIN Friend ON User.UID = Friend.UID WHERE User.UID = %s GROUP BY User.UID, User.name, User.email, User.password, User.photo"
            val = (UID, )
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            return {"UID": myresult[0][0], "name": myresult[0][1], "email": myresult[0][2], "password": myresult[0][3], "photo": myresult[0][4], "friend_count": myresult[0][5]}
        else:
            raise HTTPException(status_code=401, detail="The password is incorrect.")
    else:
        raise HTTPException(status_code=404, detail="This name or email was not found.")

@app.get("/user/{UID}")
async def getUser(UID: int):
    sql = "SELECT User.* FROM User LEFT JOIN Friend ON User.UID = Friend.friendID AND Friend.UID = %s WHERE Friend.FID IS NULL AND User.UID <> %s"
    val = (UID, UID)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    user_list = []
    for user_data in myresult:
        user_dict = {"UID": user_data[0], "name": user_data[1], "email": user_data[2], "password": user_data[3], "photo": user_data[4]}
        user_list.append(user_dict)
    return user_list

@app.get("/user/name/{name}/UID/{UID}")
async def getUsers(name: str, UID: int):
    sql = "SELECT User.* FROM User LEFT JOIN Friend ON User.UID = Friend.friendID AND Friend.UID = %s WHERE Friend.FID IS NULL AND User.UID <> %s AND User.name LIKE %s"
    NameData = '%' + name + '%'
    val = (UID, UID, NameData)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall() 
    user_list = []
    for user_data in myresult:
        user_dict = {"UID": user_data[0], "name": user_data[1], "email": user_data[2], "password": user_data[3]}
        user_list.append(user_dict)
    return user_list

@app.put("/update/user/{UID}")
async def update_User(UID : int, user_data : Request):
    user_data_json = await user_data.json()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_data_json['password'].encode(), salt) 

    sql = "UPDATE User SET name = %s, password = %s, photo = %s WHERE UID = %s"
    val = (user_data_json['name'], hashed_password, user_data_json['photo'], UID)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount == 1:
        return {"record(s) affected" : mycursor.rowcount}
    else:
        raise HTTPException(status_code=500, detail="update failed")

@app.get("/user/image/{UID}")
async def getImages(UID: int):
    sql = "SELECT Image.MID, Image.name, Image.base64, Image.UID FROM User INNER JOIN Image ON User.UID = Image.UID WHERE User.UID = %s"
    val = UID
    mycursor.execute(sql, (val, ))
    myresult = mycursor.fetchall()
    image_list = []
    for image_data in myresult:
        image_dict = {"MID": image_data[0], "name": image_data[1], "base64": image_data[2] , "UID": image_data[3]}
        image_list.append(image_dict)
    return image_list

@app.post("/user/image")
async def insert_image(user_image : User_Image):
    sql = "INSERT INTO Image (name, base64, UID) VALUES (%s, %s, %s)"
    val = (user_image.name, user_image.base64, user_image.UID)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"1 record inserted, ID:": mycursor.lastrowid}

@app.delete("/user/image/{MID}")
async def delete_image(MID: int):
    sql = "DELETE FROM Image WHERE MID = %s"
    val = (MID, )
    mycursor.execute(sql, val)
    mydb.commit()
    return {"record(s) deleted": mycursor.rowcount}

@app.post("/friend")
async def insert_friend(friend_model : Request):
    friend_model_json = await friend_model.json()
    sql = "SELECT * FROM Friend WHERE friendID = %s and UID = %s"
    val = (friend_model_json['friendID'], friend_model_json['UID'])
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if myresult:
        raise HTTPException(status_code=401, detail="Be Friend")
    else:
        sql = "INSERT INTO Friend (friendID, UID) VALUES (%s, %s)"
        val = (friend_model_json['friendID'], friend_model_json['UID'])
        mycursor.execute(sql, val)
        mydb.commit()

        sql = "INSERT INTO Friend (friendID, UID) VALUES (%s, %s)"
        val = (friend_model_json['UID'], friend_model_json['friendID'])
        mycursor.execute(sql, val)
        mydb.commit()
        return {"1 record inserted, ID:": mycursor.lastrowid}
     
@app.get("/friend/{UID}")
async def get_friend(UID: int):
    sql = "SELECT Friend.FID, Friend.friendID, User.name, User.photo FROM Friend INNER JOIN User ON Friend.friendID = User.UID WHERE Friend.UID = %s"
    val = UID
    mycursor.execute(sql, (val, ))
    myresult = mycursor.fetchall()
    friend_list = []
    for friend_data in myresult:
        friend_dict = {"FID": friend_data[0], "friendID": friend_data[1], "name": friend_data[2], "photo": friend_data[3]}
        friend_list.append(friend_dict)
    return friend_list

@app.delete("/friend")
async def delete_friend(friend_model : Request):
    friend_model_json = await friend_model.json()
    sql = "DELETE FROM Friend WHERE friendID = %s and UID = %s"
    val = (friend_model_json['friendID'], friend_model_json['UID'])
    mycursor.execute(sql, val)
    mydb.commit()

    sql = "DELETE FROM Friend WHERE friendID = %s and UID = %s"
    val = (friend_model_json['UID'], friend_model_json['friendID'])
    mycursor.execute(sql, val)
    mydb.commit()
    return {"record(s) deleted": mycursor.rowcount} 

@app.post("/massage/sent")
async def insert_massage(massage_model : Request):
    massage_model_json = await massage_model.json()
    sql = "INSERT INTO Massage (name, massage) VALUES (%s, %s)"
    val = (massage_model_json['name'], massage_model_json['massage'], )
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount == 1:
        MID = mycursor.lastrowid
        sql = "SELECT FID FROM Friend WHERE friendID = %s AND UID = %s"
        val = (massage_model_json['UID'], massage_model_json['friendID'], ) 
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            FID = myresult[0][0]
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S') 
            sql = "INSERT INTO Sent (FID, MID, time) VALUES (%s, %s, %s)"
            val = (massage_model_json['FID'], MID, formatted_datetime, )
            mycursor.execute(sql, val)
            mydb.commit()
 
            sql = "INSERT INTO Sent (FID, MID, time) VALUES (%s, %s, %s)"
            val = (FID, MID, formatted_datetime, )
            mycursor.execute(sql, val)
            mydb.commit()
            return {"record inserted.": mycursor.rowcount} 
    else:
        raise HTTPException(status_code=500, detail="insert failed")
    
@app.get("/friend/massage/{FID}")
async def get_massage(FID : int):
    sql = "SELECT Massage.MID, Massage.name, Massage.massage, Sent.time FROM Friend INNER JOIN Sent ON Friend.FID = Sent.FID INNER JOIN Massage ON Sent.MID = Massage.MID WHERE Friend.FID = %s ORDER BY Sent.time"
    val = FID
    mycursor.execute(sql, (val, ))
    myresult = mycursor.fetchall() 
    massage_list = []
    for massage_data in myresult:
        massage_dict = {"MID" : massage_data[0], "name" : massage_data[1], "massage" : massage_data[2], "time" : massage_data[3]}
        massage_list.append(massage_dict)
    return massage_list

@app.delete("/friend/massage/{MID}")
async def delete_OneMassage(MID : int):
    sql = "DELETE FROM Sent WHERE MID = %s"
    val = (MID, )
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount:
        sql = "DELETE FROM Massage WHERE MID = %s"
        val = (MID, )
        mycursor.execute(sql, val)
        mydb.commit()
        return {"record(s) deleted": mycursor.rowcount}
    else:
        raise HTTPException(status_code=500, detail="delete failed") 
    