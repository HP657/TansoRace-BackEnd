from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from Modules.Module_Basic import *
from Modules.Module_Sql import rankingSQLController
from Modules.Module_Token import jwtSystem
from Utils.Util_Handler import raise_unauthorized_exception

router = APIRouter(prefix="/component/ranking", tags=["ranking-component"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/get/my')
def get_my_ranking(current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    user_id = current_user_data['user_id']
    resultCode, resultData = rankingSQLController.getMyRanking(user_id=user_id)
    if resultCode == 200:
        return resultData


@router.get('/get/rankings')
def get_rankings(current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    resultCode, resultData = rankingSQLController.getRankings()
    if resultCode == 200:
        return resultData