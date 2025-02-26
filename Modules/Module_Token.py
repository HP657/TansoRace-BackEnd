from typing import Union
from fastapi import *
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Modules.Module_Basic import *
from Utils.Util_Env import get_env

envValue = get_env()
security = HTTPBearer()


class jwtSystem:
    SECRET_KEY = envValue.get("JWT_SECRET_KEY")
    ALGORITHM = envValue.get("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = envValue.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=jwtSystem.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, jwtSystem.SECRET_KEY, algorithm=jwtSystem.ALGORITHM
        )
        return encoded_jwt

    def verify_token(token: str):
        try:
            payload = jwt.decode(
                token, jwtSystem.SECRET_KEY, algorithms=[jwtSystem.ALGORITHM]
            )
            user_id: str = payload.get("user_id")
            if user_id is None:
                raise credentials_exception
            return user_id

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )

        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=str(e)
            )

    # JWT 검증을 위한 유틸리티 함수
    def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        user_id = jwtSystem.verify_token(token)  # 토큰을 검증하고 user_id 추출
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return {"user_id": user_id}
