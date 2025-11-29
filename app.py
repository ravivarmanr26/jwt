from fastapi import FastAPI, HTTPException, status, Request, Depends, Header
from config import * 
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from datetime import datetime,timedelta


print(PRIVATE_KEY)
print(PUBLIC_KEY)

""" 
first user going to login with user name and password then authenticate the user give access token jwt
then whenever user it tried to access other endpoints means he needs to provide the access token jwt then the system will verify the token and then process the user reuqest other won't

"""

app = FastAPI()

class UserData(BaseModel):
    username : str
    password : str


class GenerateSQlRequest(BaseModel):
    question : str

userdatabase = {
    "stevejobs" : "12345",
    "elonmusk" : "12345",
    "timcook" : "12345",
    "samaltman" : "33",
    "ironman" : "3000",
    "batman" : "22"
}

""" 
header = {algorithm and type of authentication }
payload  = { user data} + expire_time
signature = {HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)}
token = {header}

token =  " {payload} + {secret key} + {algorithm}" 
"""

def generate_token(username : str):
    expire_time = datetime.now() + timedelta(hours=EXPIRE_TIME)
    payload = {"username": username, "exp" : expire_time} 
    token = jwt.encode(payload=payload, key=PRIVATE_KEY,algorithm= ALGORITHM)
    return token

@app.post("/login")
async def login(request : UserData):
    if request.username in userdatabase and userdatabase[request.username] == request.password:
        token = generate_token(username=request.username)
        return {"Authorization" : token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")
    
def verify_token(token : str = Header()):
    try :
        payload = jwt.decode(token,PUBLIC_KEY,[ALGORITHM])
        return payload
    except InvalidTokenError as ie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = str(ie))
    
@app.post("/generate-sql")
async def generate_sql(request : GenerateSQlRequest, paylaod= Depends(verify_token)):
    username = paylaod['username']
    question = request.question
    return {"question" : question, "query" : "select * from table", "username" : username}

 
