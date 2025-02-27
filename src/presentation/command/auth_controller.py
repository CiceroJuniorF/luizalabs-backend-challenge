import base64
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from src.dependencies import oauth2_client_credentials_service
from src.infrastructure.security.oauth2_client_credentials_service import AuthenticateInput, OAuth2ClientCredentialsService
from src.presentation.command.auth_message import AuthResponse


router = APIRouter(prefix="/auth", tags=["Security"])



@router.post("/token", response_model=AuthResponse, summary="Get access token")
async def token(request: Request,  oauth2_service: OAuth2ClientCredentialsService = Depends(oauth2_client_credentials_service)) -> AuthResponse:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    encoded_credentials = auth_header[6:]
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    client_id, client_secret = decoded_credentials.split(":", 1)
    authenticate_output = oauth2_service.authenticate(AuthenticateInput.from_dict({"client_id": client_id, "client_secret": client_secret}))
    return AuthResponse(access_token = authenticate_output.access_token, token_type = authenticate_output.token_type)