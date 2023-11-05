# from typing import Union
# from fastapi import FastAPI, HTTPException, Request 
# from pydantic import BaseModel
# import numpy as np
# import base64
# import cv2
# import bcrypt
# import mysql.connector #https://www.w3schools.com/python/python_mysql_update.asp
# import datetime
# from fastapi.middleware.cors import CORSMiddleware


# # uvicorn main:app --host 192.168.111.45 --port 8000

# app = FastAPI()

# origins = [
#     "http://localhost",  # อนุญาตให้เข้าถึงจากโดเมนนี้
#     "http://localhost:8000",  # อนุญาตให้เข้าถึงจากโดเมนนี้
#     "https://yourdomain.com",  # อนุญาตให้เข้าถึงจากโดเมนนี้
#     "http://192.168.111.45:8000",
# ]

# # ตั้งค่า CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,  # อนุญาตให้ใช้งาน cookies
#     allow_methods=["*"],  # อนุญาตทุกวิธีการร้องขอ
#     allow_headers=["*"],  # อนุญาตทุกส่วนหัวในคำขอ
# )
# mydb = mysql.connector.connect(
#     host="202.28.34.197",
#     user="web65_64011212155",
#     password="64011212155@csmsu",
#     database="web65_64011212155"
# )
# mycursor = mydb.cursor()

# class User(BaseModel):
#     uname : str
#     email : str
#     password : str
    
# class Profile(BaseModel):
#     puid : str
#     pname : str
#     skill : str
#     statistics : str
#     pimg : str
    
# class Login(BaseModel):
#     lemail : str
#     lpassword : str

# class Social(BaseModel):
#     spid : str
#     message : str
#     vote : str
    
# def readb64(uri):
#    encoded_data = uri.split(',')[1] 
#    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)  
#    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#    return img

# @app.get("/")
# async def read_root():
#     return {"Hello": "Hello World !!!"}

# @app.post("/user")#สมัคu
# async def insert_user(user : User):
#     sql = "SELECT * FROM user WHERE email = %s"
#     mycursor.execute(sql, (user.email,))
#     myresult = mycursor.fetchall()
#     if myresult:
#         raise HTTPException(status_code=401, detail="Email already exists")
#     else:
#         salt = bcrypt.gensalt()
#         hashed_password = bcrypt.hashpw(user.password.encode(), salt) 
#         user.password = hashed_password

#         sql = "INSERT INTO user (uname, email, password) VALUES (%s, %s, %s)"
#         val = (user.uname, user.email, user.password)
#         mycursor.execute(sql, val)
#         mydb.commit()
#         return {"1 record inserted, ID:": mycursor.lastrowid}
    

# @app.post("/user/Login")#login
# async def user_LogIn(logIn : Login):
#     sql = "SELECT * FROM user WHERE email =%s"
#     mycursor.execute(sql,(logIn.lemail,))
#     myresult = mycursor.fetchall()
#     if myresult:
#         puid = myresult[0][0]
#         if bcrypt.checkpw(logIn.lpassword.encode(), myresult[0][3].encode()):
#             # sql = "SELECT `pid`, `puid`, `pname`, `skill`, `statistics`, `pimg` FROM `profile` WHERE puid= %s"
#             sql = "SELECT `pid`FROM profile WHERE profile.puid = %s"
#             val = (puid, )
#             mycursor.execute(sql, val)
#             myresult = mycursor.fetchall()
#             print(myresult[0])
#             return myresult[0][0]
#         else:
#             raise HTTPException(status_code=401, detail="The password is incorrect.")
#     else:
#         raise HTTPException(status_code=404, detail="This name or email was not found.")
    
# @app.get("/profile/{pid}")
# async def getdataprofile(pid: int):
#     sql = "SELECT `pid`, `pname`, `skill`, `statistics`, `pimg`,win ,loss FROM profile INNER JOIN raceresults ON profile.pid = raceresults.rpid WHERE profile.pid = %s"
#     val = pid
#     mycursor.execute(sql, (val, ))
#     myresult = mycursor.fetchall()
#     print(myresult[0][0])
#     data_profile = {"pid": myresult[0][0], "pname": myresult[0][1], "skill": myresult[0][2] , "statistics": myresult[0][3],"pimg": myresult[0][4], "win": myresult[0][5], "loss": myresult[0][6] }
#     return data_profile

# @app.post("/profile")#สมัคp
# async def insert_profile(profile : Profile):
#     sql = "SELECT * FROM profile WHERE puid = %s"
#     mycursor.execute(sql, (profile.puid,))
#     myresult = mycursor.fetchall()
#     if myresult:
#         raise HTTPException(status_code=401, detail="Email already exists")
#     else:

#         sql = "INSERT INTO `profile`(`puid`, `pname`, `skill`, `statistics`, `pimg`) VALUES (%s,%s,%s,0,%s)"
#         val = (profile.puid, profile.pname, profile.skill,profile.pimg)
#         mycursor.execute(sql, val)        
#         mydb.commit()
#         return {"1 record inserted, ID:": mycursor.lastrowid}
        
# @app.put("/update/profile/{pid}")#update_profile
# async def update_profile(pid : int, profile_data : Request):
#     profile_json = await profile_data.json()

#     sql = "UPDATE `profile` SET `pname`=%s,`skill`=%s,`pimg`=%s WHERE pid=%s"
#     val = (profile_json['pname'], profile_json['skill'], profile_json['pimg'], pid)
#     mycursor.execute(sql, val)
#     mydb.commit()
#     if mycursor.rowcount == 1:
#         return {"record(s) affected" : mycursor.rowcount}
#     else:
#         raise HTTPException(status_code=500, detail="update failed")
    
# @app.get("/social")#SELECT social
# async def getsocial():
#     sql = "SELECT `sid`, `spid`, `message`, `pimg`, `vote`,pname FROM `social` INNER JOIN profile ON social.spid = profile.pid"
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall() 
#     social_list = []
#     for social_data in myresult:
#         user_dict = {"sid": social_data[0], "spid": social_data[1], "message": social_data[2], "pimg": social_data[3], "vote": social_data[4],"pname":social_data[5]}
#         social_list.append(user_dict)
#     return social_list

# @app.post("/social")#เพิ่มsocial
# async def insert_social(social : Social):
#     sql = "INSERT INTO social (spid, message,simg, vote) VALUES (%s, %s, %s, %s)"
#     s="https://www.alleycat.org/wp-content/uploads/2019/03/FELV-cat.jpg"
    
#     val = (social.spid, social.message,s, social.vote)
#     mycursor.execute(sql, val)
#     mydb.commit()
#     return {"1 record inserted, ID:": mycursor.lastrowid}

# @app.put("/update/social/vote/{sid}")#update_vote
# async def update_social(sid : int):
#     sql = "SELECT `sid`,`vote` FROM `social` WHERE sid = %s"
#     mycursor.execute(sql, (sid,))
#     myresult = mycursor.fetchall()
#     print(myresult[0])
#     if myresult:
#         sql = "UPDATE `social` SET `vote`=%s WHERE sid=%s"
#         vote=myresult[0][1]+1
#         val = (vote,sid)
#         mycursor.execute(sql, val)        
#         mydb.commit()
#         return {"1 record inserted, ID:": mycursor.lastrowid}
    
# @app.delete("/friend/social/{sid}")
# async def delete_OneMassage(sid : int):
#     sql = "DELETE FROM social WHERE MID = %s"
#     val = (sid, )
#     mycursor.execute(sql, val)
#     mydb.commit()
#     if mycursor.rowcount:
#         sql = "DELETE FROM social WHERE MID = %s"
#         val = (sid, )
#         mycursor.execute(sql, val)
#         mydb.commit()
#         return {"record(s) deleted": mycursor.rowcount}
#     else:
#         raise HTTPException(status_code=500, detail="delete failed") 
    


#ver2
from typing import Union
from fastapi import FastAPI, HTTPException, Request 
from pydantic import BaseModel
import numpy as np
import base64
import cv2
import bcrypt
import mysql.connector #https://www.w3schools.com/python/python_mysql_update.asp
import datetime
from fastapi.middleware.cors import CORSMiddleware


# uvicorn main:app --host 192.168.111.45 --port 8000

app = FastAPI()

origins = [
    "http://localhost",  # อนุญาตให้เข้าถึงจากโดเมนนี้
    "http://localhost:8000",  # อนุญาตให้เข้าถึงจากโดเมนนี้
    "https://yourdomain.com",  # อนุญาตให้เข้าถึงจากโดเมนนี้
    "http://192.168.111.45:8000",
]

# ตั้งค่า CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # อนุญาตให้ใช้งาน cookies
    allow_methods=["*"],  # อนุญาตทุกวิธีการร้องขอ
    allow_headers=["*"],  # อนุญาตทุกส่วนหัวในคำขอ
)
mydb = mysql.connector.connect(
    host="202.28.34.197",
    user="web65_64011212155",
    password="64011212155@csmsu",
    database="web65_64011212155"
)
mycursor = mydb.cursor()

class User(BaseModel):
    uname : str
    email : str
    password : str
    
class Profile(BaseModel):
    puid : str
    pname : str
    skill : str
    statistics : str
    pimg : str
    
class Login(BaseModel):
    lemail : str
    lpassword : str

class Social(BaseModel):
    spid : str
    message : str
    vote : str
class Raceresults(BaseModel):
    pid1 : str
    pid2 : str
    winloss : str
    
    
def readb64(uri):
   encoded_data = uri.split(',')[1] 
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)  
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

@app.get("/")
async def read_root():
    return {"Hello": "Hello World !!!"}

@app.post("/user")#สมัคu
async def insert_user(user : User):
    sql = "SELECT * FROM user WHERE email = %s"
    mycursor.execute(sql, (user.email,))
    myresult = mycursor.fetchall()
    if myresult:
        raise HTTPException(status_code=401, detail="Email already exists")
    else:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode(), salt) 
        user.password = hashed_password

        sql = "INSERT INTO user (uname, email, password) VALUES (%s, %s, %s)"
        val = (user.uname, user.email, user.password)
        mycursor.execute(sql, val)
        mydb.commit()
        return {mycursor.lastrowid}
    

@app.post("/user/Login")#login
async def user_LogIn(logIn : Login):
    sql = "SELECT * FROM user WHERE email =%s"
    mycursor.execute(sql,(logIn.lemail,))
    myresult = mycursor.fetchall()
    if myresult:
        puid = myresult[0][0]
        if bcrypt.checkpw(logIn.lpassword.encode(), myresult[0][3].encode()):
            # sql = "SELECT `pid`, `puid`, `pname`, `skill`, `statistics`, `pimg` FROM `profile` WHERE puid= %s"
            sql = "SELECT `pid`FROM profile WHERE profile.puid = %s"
            val = (puid, )
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            print(myresult[0])
            return myresult[0][0]
        else:
            raise HTTPException(status_code=401, detail="The password is incorrect.")
    else:
        raise HTTPException(status_code=404, detail="This name or email was not found.")
    
@app.get("/profile/{pid}")
async def getdataprofile(pid: int):
    sql = "SELECT `pid`, `pname`, `skill`,(win+loss)as statistics, `pimg`,win ,loss FROM profile INNER JOIN raceresults ON profile.pid = raceresults.rpid WHERE profile.pid = %s"
    val = pid
    mycursor.execute(sql, (val, ))
    myresult = mycursor.fetchall()
    print(myresult[0][0])
    data_profile = {"pid": myresult[0][0], "pname": myresult[0][1], "skill": myresult[0][2] , "statistics": myresult[0][3],"pimg": myresult[0][4], "win": myresult[0][5], "loss": myresult[0][6] }
    return data_profile

@app.get("/profileall")
async def getdataprofileall():
    sql = "SELECT pid, pname, skill,(win+loss)as statistics, pimg,win ,loss FROM profile INNER JOIN raceresults ON profile.pid = raceresults.rpid"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    profileall = []
    for profil in myresult:
        user_dict = {"pid": profil[0], "pname": profil[1], "skill": profil[2] , "statistics": profil[3],"pimg": profil[4], "win": profil[5], "loss": profil[6] }
        profileall.append(user_dict)
    return profileall



@app.post("/profile")#สมัคp
async def insert_profile(profile : Profile):
    sql = "SELECT * FROM profile WHERE puid = %s"
    mycursor.execute(sql, (profile.puid,))
    myresult = mycursor.fetchall()
    if myresult:
        raise HTTPException(status_code=401, detail="Email already exists")
    else:

        sql = "INSERT INTO `profile`(`puid`, `pname`, `skill`, `statistics`, `pimg`) VALUES (%s,%s,%s,0,%s)"
        val = (profile.puid, profile.pname, profile.skill,profile.pimg)
        mycursor.execute(sql, val) 
        pid=mycursor.lastrowid   
        sql = "INSERT INTO `raceresults`(`rpid`, `win`, `loss`) VALUES (%s,0,0)"
        val = (mycursor.lastrowid ,)
        mycursor.execute(sql, val)     
        mydb.commit()
        return {"1 record inserted, ID:": pid}
        
@app.put("/update/profile/{pid}")#update_profile
async def update_profile(pid : int, profile_data : Request):
    profile_json = await profile_data.json()

    sql = "UPDATE `profile` SET `pname`=%s,`skill`=%s,`pimg`=%s WHERE pid=%s"
    val = (profile_json['pname'], profile_json['skill'], profile_json['pimg'], pid)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount == 1:
        return {"record(s) affected" : mycursor.rowcount}
    else:
        raise HTTPException(status_code=500, detail="update failed")
    
@app.get("/social")#SELECT social
async def getsocial():
    sql = "SELECT `sid`, `spid`, `message`, `pimg`, `vote`,pname FROM `social` INNER JOIN profile ON social.spid = profile.pid"
    mycursor.execute(sql)
    myresult = mycursor.fetchall() 
    social_list = []
    for social_data in myresult:
        user_dict = {"sid": social_data[0], "spid": social_data[1], "message": social_data[2], "pimg": social_data[3], "vote": social_data[4],"pname":social_data[5]}
        social_list.append(user_dict)
    return social_list

@app.post("/social")#เพิ่มsocial
async def insert_social(social : Social):
    sql = "INSERT INTO social (spid, message,simg, vote) VALUES (%s, %s, %s, %s)"
    s="https://www.alleycat.org/wp-content/uploads/2019/03/FELV-cat.jpg"
    
    val = (social.spid, social.message,s, social.vote)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"1 record inserted, ID:": mycursor.lastrowid}

@app.put("/update/social/vote/{sid}")#update_vote
async def update_social(sid : int):
    sql = "SELECT `sid`,`vote` FROM `social` WHERE sid = %s"
    mycursor.execute(sql, (sid,))
    myresult = mycursor.fetchall()
    print(myresult[0])
    if myresult:
        sql = "UPDATE `social` SET `vote`=%s WHERE sid=%s"
        vote=myresult[0][1]+1
        val = (vote,sid)
        mycursor.execute(sql, val)        
        mydb.commit()
        return {"1 record inserted, ID:": mycursor.lastrowid}
    
@app.delete("/friend/social/{sid}")
async def delete_Onepost(sid : int):
    sql = "DELETE FROM social WHERE sid = %s"
    val = (sid, )
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount:
        sql = "DELETE FROM social WHERE sid = %s"
        val = (sid, )
        mycursor.execute(sql, val)
        mydb.commit()
        return {"record(s) deleted": mycursor.rowcount}
    else:
        raise HTTPException(status_code=500, detail="delete failed") 
    
@app.put("/update/raceresults")#update_raceresults
async def update_raceresults(raceresults : Raceresults):
    sql = "SELECT `win`, `loss` FROM `raceresults` WHERE rpid=%s"
    mycursor.execute(sql,(raceresults.pid1,))
    myresult = mycursor.fetchall()
    print(myresult[0])
    win1=myresult[0][0]
    loss1=myresult[0][1]
    
    sql = "SELECT `win`, `loss` FROM `raceresults` WHERE rpid=%s"
    mycursor.execute(sql,(raceresults.pid2,))
    myresult = mycursor.fetchall()
    win2=myresult[0][0]
    loss2=myresult[0][1]
    if raceresults.winloss==0:
        sql = "UPDATE `raceresults` SET `win`=%s WHERE rpid=%s"
        win=win1+1
        val = (win,raceresults.pid1)
        mycursor.execute(sql, val)
        sql = "UPDATE `raceresults` SET `loss`=%s WHERE rpid=%s"
        loss=loss2+1
        val = (loss,raceresults.pid2)
        mycursor.execute(sql, val)        
        mydb.commit()
        return {"1 record inserted, ID:": mycursor.lastrowid}
    else :
        sql = "UPDATE `raceresults` SET `loss`=%s WHERE rpid=%s"
        loss=loss1+1
        val = (loss,raceresults.pid1)
        mycursor.execute(sql, val)
        sql = "UPDATE `raceresults` SET `win`=%s WHERE rpid=%s"
        win=win2+1
        val = (win,raceresults.pid2)
        mycursor.execute(sql, val)        
        mydb.commit()
        return {"1 record inserted, ID:": mycursor.lastrowid}