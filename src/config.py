import os
from dotenv import load_dotenv

load_dotenv()

USE_IN_MEMORY = bool(int(os.getenv('USE_IN_MEMORY', 0)))
SECURITY_OAUTH2_JWT_SECRET=os.getenv('SECURITY_OAUTH2_JWT_SECRET', "dev_secret")
SECURITY_OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv('SECURITY_OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES', 30))
SECURITY_OAUTH2_JWT_ALGORITHM=os.getenv('SECURITY_OAUTH2_JWT_ALGORITHM', "HS256")

CLIENT_ID=os.getenv('CLIENT_ID', "luizalabs")
CLIENT_SECRET=os.getenv('CLIENT_SECRET', "client_secret")

MONGODB_URL=os.getenv('MONGODB_URL', "mongodb://localhost:27017")
MONGODB_DB=os.getenv('MONGODB_DB', "luizalabs")
MONGODB_USERNAME=os.getenv('MONGODB_USERNAME', "root")
MONGODB_PASSWORD=os.getenv('MONGODB_PASSWORD', "root")