import pytest
from datetime import datetime, timedelta
from jose import jwt, JWTError
from src.infrastructure.security.oauth2_client_credentials_service import AccessTokenInput, OAuth2ClientCredentialsService
import src.config as config

def test_should_create_jwt_token():
    service = OAuth2ClientCredentialsService()
    data = {"sub": "test"}
    expires_delta = timedelta(minutes=5)
    expire = datetime.now() + expires_delta
    token = service.create_jwt_token(data, expire)
    assert token is not None
    decoded_data = jwt.decode(token, config.SECURITY_OAUTH2_JWT_SECRET, algorithms=[config.SECURITY_OAUTH2_JWT_ALGORITHM])
    assert decoded_data["sub"] == "test"
    assert "exp" in decoded_data

def test_shouldnt_create_jwt_token_because_invalid_secret():
    service = OAuth2ClientCredentialsService()
    data = {"sub": "test"}
    expires_delta = timedelta(minutes=5)
    expire = datetime.now() + expires_delta
    token = service.create_jwt_token(data, expire)
    try:
        jwt.decode(token, "invalid_secret", algorithms=[config.SECURITY_OAUTH2_JWT_ALGORITHM])
    except JWTError as e:
        assert "Signature verification failed." in str(e)

def test_should_decode_jwt_token():
    service = OAuth2ClientCredentialsService()
    data = {"sub": "test"}
    expires_delta = timedelta(minutes=5)
    expire = datetime.now() + expires_delta
    token = service.create_jwt_token(data, expire)
    decoded_data = service.decode_jwt_token(token)
    assert decoded_data["sub"] == "test"
    assert "exp" in decoded_data

def test_shouldnt_decode_jwt_token_because_expired():
    service = OAuth2ClientCredentialsService()
    data = {"sub": "test"}
    expires_delta = timedelta(seconds=-1)
    expire = datetime.now() + expires_delta
    token = service.create_jwt_token(data, expire)
    try:
        service.decode_jwt_token(token)
    except JWTError as e:
        assert "Signature has expired." in str(e)

def test_shouldnt_decode_jwt_token_because_invalid_token():
    service = OAuth2ClientCredentialsService()
    invalid_token = "invalid.token.value"
    
    try:
        service.decode_jwt_token(invalid_token)
    except JWTError as e:
        assert "Invalid" in str(e)

def test_should_create_access_token():
    service = OAuth2ClientCredentialsService()
    input_data = {"client_id": config.CLIENT_ID, "client_secret": config.CLIENT_SECRET}
    access_token_input = AccessTokenInput.from_dict(input_data)
    access_token_output = service.create_access_token(access_token_input)
    assert access_token_output.access_token is not None
    assert access_token_output.token_type == "bearer"
    assert access_token_output.expires_in is not None
    decoded_data = jwt.decode(access_token_output.access_token, config.SECURITY_OAUTH2_JWT_SECRET, algorithms=[config.SECURITY_OAUTH2_JWT_ALGORITHM])
    assert decoded_data["sub"] == config.CLIENT_ID
    assert "exp" in decoded_data

def test_should_authorize():
    service = OAuth2ClientCredentialsService()
    data = {"sub": config.CLIENT_ID}
    expires_delta = timedelta(minutes=5)
    expire = datetime.now() + expires_delta
    token = service.create_jwt_token(data, expire)
    assert service.authorize(token)

def test_shouldnt_authorize_because_invalid_token():
    invalid_token = "invalid.token.value"
    service = OAuth2ClientCredentialsService()
    try:
        service.authorize(invalid_token)
    except JWTError as e:
        assert "Invalid" in str(e)

def test_shouldnt_authorize_because_expired_token():
    service = OAuth2ClientCredentialsService()
    data = {"sub": config.CLIENT_ID}
    expires_delta = timedelta(seconds=-1)
    expire = datetime.now() + expires_delta
    token = service.create_jwt_token(data, expire)
    try:
        service.authorize(token)
    except JWTError as e:
        assert "Signature has expired." in str(e)

def test_shouldnt_authorize_because_isnt_CLIENT_ID():
    service = OAuth2ClientCredentialsService()
    data = {"sub": "any"}
    expires_delta = timedelta(seconds=10)
    expire = datetime.now() + expires_delta
    token = service.create_jwt_token(data, expire)
    try:
        service.authorize(token)
    except JWTError as e:
        assert "Unauthorized" in str(e)
    


