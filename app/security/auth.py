import time
import jwt

from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from configs import JWT_SECRET, JWT_ALGORITHM, JWT_COOKIE

JWT_LIFETIME = 60*60*24  # seconds


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


class JWTBase:

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decode_jwt_token(jwtoken)
            return True if payload else False
        except Exception:
            return False


class JWTBearer(HTTPBearer, JWTBase):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials


class JWTCookieAuth(JWTBase):

    def __init__(self):
        pass

    async def __call__(self, request: Request):
        jwtoken = self.get_jwt_from_cookie(request)
        if not jwtoken:
            raise HTTPException(status_code=403, detail="Invalid authorization.")
        if not self.verify_jwt(jwtoken):
            raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        return jwtoken

    def get_jwt_from_cookie(self, request: Request):
        if 'cookie' not in request.headers:
            raise HTTPException(status_code=403, detail="No session token found.")
        jwt_cookie = request.headers['cookie'].split(f'{JWT_COOKIE}=')
        if jwt_cookie:
            return jwt_cookie[1]
        return ''
