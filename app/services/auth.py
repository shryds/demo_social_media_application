import datetime 
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.environ.get("SECRET_KEY")

ALG="HS256"
EXPIRY_TIME = 40000

def create_access_token(data):
    expire = datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=EXPIRY_TIME)    
    data["exp"] = expire
    token=jwt.encode(data,SECRET_KEY,ALG)
    return token
    
    
def decode_token(jwt_token: str):
    decoded_token= jwt.decode(jwt_token,SECRET_KEY,ALG)
    return decoded_token

