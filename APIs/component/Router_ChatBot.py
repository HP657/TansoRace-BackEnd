from fastapi import *
from fastapi.security import OAuth2PasswordBearer

from APIs.component.Controllers import Controller_ChatBot

from Modules.Module_Sql import chatbotSQLController
from Modules.Module_ai import *
from Modules.Module_Token import jwtSystem

from Utils.Util_Handler import raise_unauthorized_exception

router = APIRouter(prefix="/component/chat-bot", tags=["chatBot-component"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/chat")
def aiChat(chatData: Controller_ChatBot.controllerChatBot_Chat, current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")

    load_env()
    model = get_model()
    df = get_dataset()

    user_id = current_user_data['user_id']
    user_text = chatData.user_text

    embedding = model.encode(user_text)

    df["distance"] = df["embedding"].map(
        lambda x: cosine_similarity([embedding], [x]).squeeze()
    )

    answer = df.loc[df["distance"].idxmax()]
    if answer["distance"] > 0.75:
        return {
            "result": True,
            "message": "정상적으로 완료 되었습니다.",
            "chatBot": json.loads(answer["챗봇"]),
            "distance": answer["distance"],
        }
    else:
        chatbotSQLController.insertLogData(user_id=user_id, user_text=user_text, user_distance=answer["distance"])
        return {
            "result": True,
            "message": "정상적으로 완료 되었습니다.",
            "chatBot": "학습 데이터 생성을 위해 공부중 이에요! 최대한 빠르게 반영 해드릴게요!!",
            "distance": answer["distance"],
        }
