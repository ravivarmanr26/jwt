from fastapi import FastAPI,HTTPException,status
from datetime import datetime,timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from core.config import *
app = FastAPI()

""" 
header = {algorithm and type of authentication }
payload  = { user data} + expiretime
signature = {HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)}
token = {header}

token =  " {payload} + {secret key} + {algorithm}" 
"""

userdatabase ={
    'stevejobs' : '12345',
    'billgates' : '12345',
    'mark zuckerberg': '32423'
}

def create_token(username: str):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=EXPIRE_TIME)
    payload = {"username":username, "exp": expire.timestamp()}
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

    return token
    

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Access payload fields
        user_id = payload.get("username")

        print("Payload:", payload)
        print("User ID:", user_id)
        return payload
    except InvalidTokenError as ie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = str(ie))
    
@app.get("/")
def hello():
    return {"message":"the server is alive"}

@app.post("/login")
def user_login(username:str, password: str):
    try:
        if username in userdatabase and userdatabase[username] == password:
            token = create_token(username=username)
            return {"message": "you are verified user",  "token": token }
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    except HTTPException :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" the request is bad")
        
    
@app.get("/home")
def home_page(token:str):
    payload = verify_token(token)
    username = payload["username"]
    if username in userdatabase:
        return {"message" :"welcome {username} to home page"}
    

