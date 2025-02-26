from fastapi import *
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from Modules.Module_Basic import *
from Modules.Module_Sql import pointSQLController
from Modules.Module_Token import jwtSystem
from Utils.Util_Handler import raise_unauthorized_exception
from APIs.sales.Controllers import Controller_Point


router = APIRouter(prefix="/sales/point", tags=["sales-point"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/get")
def sales_point_get(current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    result_code, result_data = pointSQLController.getUserPoint(user_id)

    if result_code == 200:
        return {"result": True, "data": result_data}

    return {"result": False, "message": result_data}
    

@router.post("/set")
def sales_point_set(pointData: Controller_Point.controllerPoint_Set, current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    result_code, result_data = pointSQLController.setUserPointSet(user_id=user_id, point_count=pointData.point)

    if result_code == 200:
        return {"result": True, "data": result_data}

    return {"result": False, "message": result_data}


@router.post("/update")
def sales_point_update(pointData: Controller_Point.controllerPoint_Update, current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    result_code, result_data = pointSQLController.updateUserPoint(input_type=str(pointData.input_type),user_id=user_id, point_count=pointData.point)

    if result_code == 200:
        return {"result": True, "data": result_data}

    return {"result": False, "message": result_data}