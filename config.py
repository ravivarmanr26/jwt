ALGORITHM = 'RS256'
EXPIRE_TIME = 1

with open("private.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("public.pem", "r") as f:
    PUBLIC_KEY = f.read()