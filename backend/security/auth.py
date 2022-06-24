import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class _AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def encode_jwt_token(self, user_id):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=30),
            "iat" : datetime.utcnow(),
            "scope" : "access_token",
            "sub" : user_id
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_jwt_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="JTW token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def encode_refresh_token(self, username: str) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=1),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def refresh_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                username = payload['sub']
                return self.encode_jwt_token(username)
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')


AuthHandler = _AuthHandler()

