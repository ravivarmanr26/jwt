from fastapi import FastAPI,HTTPException,status
from datetime import datetime,timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from config import *
app = FastAPI()

""" 
header = {algorithm and type of authentication }
payload  = { user data}
signature = {HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)}
token = {header}
"""

userdatabase ={
    'stevejobs' : '12345',
    'billgates' : '12345',
    'mark zuckerberg': '32423'
}

def create_token(username: str):
    expire = datetime.utcnow()+timedelta(minutes=EXPIRE_TIME)
    payload = {"username":username, "expire_time": expire.timestamp()}
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token
    

def verify_token(token:str):
    try:
        t = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return t
    except InvalidTokenError as ie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="the token is expired")
    
@app.get("/")
def hello():
    return {"message":"the server is alive"}

@app.post("/login")
def user_login(username:str, password: str):
    try:
        if username in userdatabase and userdatabase[username] == password:
            token = create_token(username=username)
            return {f"message:","you are verified user",  f"token :{token}"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    except HTTPException :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" the request is bad")
        
    
@app.get("/home")
def home_page(token:str):
    payload = verify_token(token)
    username = payload["username"]
    if username in userdatabase:
        return {"message" :f"welcome {username} to home page"}
    

        

