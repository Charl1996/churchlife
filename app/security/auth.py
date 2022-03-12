import time
import jwt

from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from configs import JWT_SECRET, JWT_ALGORITHM

JWT_LIFETIME = 60*60  # seconds


def generate_jwt_token(data: dict) -> str:
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt_token(encoded_jwt: str) -> any:
    try:
        decoded_data = jwt.decode(encoded_jwt, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_data if decoded_data['expires'] >= time.time() else None
    except:
        return None


def sign_jwt(data: dict) -> dict:
    expirable_data = {
        'expires': time.time() + JWT_LIFETIME,
        **data
    }

    return generate_jwt_token(expirable_data)


class AuthRequest(HTTPBearer):

    @classmethod
    async def authorize(cls, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        breakpoint()
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail="Invalid authorization scheme.")

            payload = cls.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

        # add payload to request somehow
        request_body = await request.json()
        return request

    @classmethod
    def verify_jwt(cls, jwtoken: str) -> bool:
        try:
            payload = decode_jwt_token(jwtoken)
            return payload
        except Exception:
            return False
