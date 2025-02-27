from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import src.config as config
from jose import JWTError, jwt

@dataclass
class AuthenticateInput:
    client_id: str
    client_secret: str

    @classmethod
    def from_dict(cls, input_value):
        instance =  cls(**input_value)
        return instance
    
@dataclass
class AuthenticateOutput:
    access_token: str
    token_type: str
    expires_in: int
    @classmethod
    def from_dict(cls, input_value):
        instance =  cls(**input_value)
        return instance

    def to_dict(self) -> dict:
        return asdict(self)


class OAuth2ClientCredentialsService:

    def create_jwt_token(self, data: dict, expire: datetime):
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, config.SECURITY_OAUTH2_JWT_SECRET, algorithm=config.SECURITY_OAUTH2_JWT_ALGORITHM)
    
    def decode_jwt_token(self, token: str):
        return jwt.decode(token, config.SECURITY_OAUTH2_JWT_SECRET, algorithms=[config.SECURITY_OAUTH2_JWT_ALGORITHM])
    

    def authenticate(self, input: AuthenticateInput) -> AuthenticateOutput:
        data = {"sub": input.client_id}
        if(input.client_id != config.CLIENT_ID or input.client_secret != config.CLIENT_SECRET):
            raise JWTError("Unauthorized")
        expires_delta = timedelta(minutes=config.SECURITY_OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now() + expires_delta
        access_token = self.create_jwt_token(data, expire)
        return AuthenticateOutput.from_dict({"access_token": access_token, "token_type": "bearer", "expires_in": expire.timestamp()})
    
    def authorize(self, access_token:str) -> bool:
        print(access_token)
        decoded = jwt.decode(access_token, config.SECURITY_OAUTH2_JWT_SECRET, algorithms=[config.SECURITY_OAUTH2_JWT_ALGORITHM])
        if(decoded["sub"] != config.CLIENT_ID):
            raise JWTError("Unauthorized")
        return True
    
