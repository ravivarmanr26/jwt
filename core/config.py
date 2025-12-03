ALGORITHM = 'RS256'
EXPIRE_TIME = 1

import os 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "..", "keys", "private.pem")
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "..", "keys", "public.pem")

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()