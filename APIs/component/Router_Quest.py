from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from Modules.Module_Basic import *
from Modules.Module_Sql import questSQLController
from Modules.Module_Token import jwtSystem
from APIs.component.Controllers import Controller_Quest
from Utils.Util_Handler import raise_unauthorized_exception

router = APIRouter(prefix="/component/quest", tags=["quest-component"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/get")
def sales_point_get(current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    result_code, result_data = questSQLController.getUserQuest(user_id)

    if result_code == 200:
        return {"result": True, "data": result_data}

    return {"result": False, "message": result_data}
    

@router.get("/get/today")
def sales_point_get(current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    result_code, result_data = questSQLController.getUserToDayQuest(user_id)

    if result_code == 200:
        return {"result": True, "data": result_data}

    return {"result": False, "message": result_data}


@router.post("/set")
def quest_count_set(questData: Controller_Quest.controllerQuestCount_Set, current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    result_code, result_data = questSQLController.setUserQuest(user_id=user_id, quest_point=questData.count)

    if result_code == 200:
        return {"result": True, "data": result_data}

    return {"result": False, "message": result_data}


@router.post("/update")
def quest_count_update(questData: Controller_Quest.controllerQuestCount_Update, current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    result_code, result_data = questSQLController.updateUserQuest(input_type=str(questData.input_type),user_id=user_id, quest_point=questData.count)

    if result_code == 200:
        return {"result": True, "data": result_data}

    return {"result": False, "message": result_data}


@router.post("/clear")
def sales_point_clear(questData: Controller_Quest.controllerQuest_Clear, current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    result_code, result_data = questSQLController.clearUserQuest(user_id=user_id, clearQuestName=questData.quest_name)

    if result_code == 200:
        return {"result": True, "data": result_data}

    return {"result": False, "message": result_data}