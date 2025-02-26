from fastapi import *
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from Modules.Module_Basic import *
from Modules.Module_Sql import authSQLController
from Modules.Module_Token import jwtSystem
from APIs.company.Controllers import Controller_Auth

router = APIRouter(prefix="/company/auth", tags=["company-auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
def company_authLogin(loginData: Controller_Auth.controllerAuth_Login):
    resultCode, resultData = authSQLController.checkUserData(
        loginData.user_id, loginData.user_pw
    )
    if resultCode == 200:
        access_token_expires = timedelta(minutes=jwtSystem.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = jwtSystem.create_access_token(
            data={"user_id": loginData.user_id, "user_role": resultData["user_role"]},
            expires_delta=access_token_expires,
        )
        return {
            "result": True,
            "user_id": loginData.user_id,
            "access_token": access_token,
        }

    return {"result": False, "message": resultData}


@router.post("/register")
def company_authRegister(registerData: Controller_Auth.controllerAuth_Register):
    resultCode, resultData = authSQLController.insertUserData(registerData)
    if resultCode == 200:
        raise HTTPException(
            status_code=resultCode,
            detail=resultData,
        )
        # return {"result": True, "user_id": registerData.user_id, "message": resultData}

    raise HTTPException(
        status_code=resultCode,
        detail=resultData,
    )


@router.delete("/deleteUser/{user_id}")
def company_deleteUser(
    user_id: str, current_userData: str = Depends(jwtSystem.get_current_user)
):
    if not current_userData:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인을 해주시기 바랍니다.",
        )

    resultCode, resultData = authSQLController.deleteUserData(user_id)
    if resultCode == 200:
        return {"result": True, "user_id": resultData}

    return {"result": False, "message": resultData}


@router.get("/user/{user_id}")
def company_getUser(
    user_id: str, current_userData: str = Depends(jwtSystem.get_current_user)
):
    if not current_userData:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인을 해주시기 바랍니다.",
        )

    resultCode, resultData = authSQLController.getUserData(user_id)
    if resultCode == 200:
        return {"result": True, "users": resultData}

    return {"result": False, "message": resultData}


@router.get("/users")
def company_authUsers(current_userData: str = Depends(jwtSystem.get_current_user)):
    if not current_userData:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인을 해주시기 바랍니다.",
        )

    resultCode, resultData = authSQLController.getUsersData()
    if resultCode == 200:
        return {"result": True, "users": resultData}

    return {"result": False, "message": resultData}
