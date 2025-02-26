from fastapi import *
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from Modules.Module_Basic import *
from Modules.Module_Sql import authSQLController, envValue
from Modules.Module_Token import jwtSystem
from Utils.Util_Env import get_env
from APIs.sales.Controllers import Controller_Auth
from Utils.Util_Handler import raise_unauthorized_exception

router = APIRouter(prefix="/sales/auth", tags=["sales-auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
envValue = get_env()


@router.get("/check/token")
def sales_auth_check_toeken(current_userData: str = Depends(jwtSystem.get_current_user)):
    if not current_userData:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"result": False, "message": "로그인을 해주시기 바랍니다."},
        )

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail={"result": True, "message": "정상 토큰."},
    )


@router.post("/login")
def sales_authLogin(loginData: Controller_Auth.controllerAuth_Login):
    resultCode, resultData = authSQLController.checkUserData(loginData.user_id, loginData.user_pw)
    if resultCode == 200:
        access_token_expires = timedelta(minutes=int(envValue.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')))
        access_token = jwtSystem.create_access_token(
            data={"user_id": loginData.user_id},
            expires_delta=access_token_expires,
        )
        return {
            "result": True,
            "user_id": loginData.user_id,
            "access_token": access_token,
        }

    return {"result": False, "message": resultData}


@router.post("/register")
def sales_authRegister(registerData: Controller_Auth.controllerAuth_Register):
    resultCode, resultData = authSQLController.insertUserData(registerData)
    if resultCode == 200:
        return {"result": True, "user_id": registerData.user_id, "message": resultData}

    return {"result": False, "message": resultData}


@router.get("/user")
def sales_getUser(current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    resultCode, resultData = authSQLController.getUserData(user_id = current_user_data['user_id'])
    if resultCode == 200:
        raise HTTPException(
            status_code=resultCode,
            detail=resultData,
        )

    raise HTTPException(
        status_code=resultCode,
        detail=resultData,
    )


@router.get("/users")
def sales_authUsers(current_userData: str = Depends(jwtSystem.get_current_user)):
    if not current_userData:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인을 해주시기 바랍니다.",
        )

    resultCode, resultData = authSQLController.getUsersData()
    if resultCode == 200:
        return {"result": True, "users": resultData}

    return {"result": False, "message": resultData}
