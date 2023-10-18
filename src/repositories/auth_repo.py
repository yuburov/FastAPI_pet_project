from datetime import datetime, timedelta
from typing import Optional

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, exceptions

from src.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, JWT_SECRET_KEY, \
    JWT_REFRESH_SECRET_KEY


class JWTRepo:

    def __init__(self, data: dict = {}, token: str = None):
        self.data = data
        self.token = token

    def generate_token(self, secret_key: str, expires_delta: Optional[timedelta] = None):
        return self._generate_jwt(secret_key, expires_delta)

    def generate_refresh_token(self, secret_key: str, expires_delta: Optional[timedelta] = None):
        # Устанавливаем срок действия refresh token (по умолчанию 30 дней)
        expires_delta = expires_delta or timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
        return self._generate_jwt(secret_key, expires_delta)

    def _generate_jwt(self, secret_key: str, expires_delta: timedelta):
        to_encode = self.data.copy()
        expire = datetime.utcnow() + (
                    expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))  # Default expiration: 15 minutes
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

        return encode_jwt

    def decode_token(self, secret_key: str):
        try:
            decode_token = jwt.decode(
                self.token, secret_key, algorithms=[ALGORITHM])
            return decode_token if decode_token["exp"] >= datetime.utcnow() else None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def extract_token(token: str, secret_key: str):
        return jwt.decode(token, secret_key, algorithms=[ALGORITHM])


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authorization code."})

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = jwt.decode(jwtoken, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            is_token_valid = True
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except exceptions.JWTError:
            print("Invalid token.")
        except Exception as e:
            print(f"An error occurred while decoding the token: {str(e)}")

        if not is_token_valid:
            try:
                payload = jwt.decode(jwtoken, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
                is_token_valid = True
            except jwt.ExpiredSignatureError:
                print("Refresh token has expired.")
            except exceptions.JWTError:
                print("Invalid refresh token.")
            except Exception as e:
                print(f"An error occurred while decoding the refresh token: {str(e)}")

        return is_token_valid


jwt_bearer = JWTBearer()
