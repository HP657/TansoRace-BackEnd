from fastapi import *
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from Utils.Util_Env import get_env

from Modules.Module_Basic import *

from APIs.company import Router_c_Auth
from APIs.sales import Router_Auth
from APIs.sales import Router_Point
from APIs.component import Router_ImageAI
from APIs.component import Router_Quest
from APIs.component import Router_Ranking
from APIs.component import Router_ChatBot

envValue = get_env()

app = FastAPI(
    title="Daejin Tanso API",
    description="대진전자통신고등학교 탄소레이스 API SERVER 입니다.",
    version="0.1.0",

    swagger_ui_parameters={
        "operationsSorter": "method"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# company
app.include_router(Router_c_Auth.router)

# sales
app.include_router(Router_Auth.router)
app.include_router(Router_Point.router)

# component
app.include_router(Router_ImageAI.router)
app.include_router(Router_Quest.router)
app.include_router(Router_Ranking.router)
app.include_router(Router_ChatBot.router)

@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("./favicon.ico")


if __name__ == "__main__":
    print(f'http://{envValue.get("SERVER_HOST")}:{envValue.get("SERVER_PORT")}/docs')
    uvicorn.run(  # cmd: tree D:\GitHub\daejin.tanso.server
        "app:app",
        host=envValue.get("SERVER_HOST"),
        port=int(envValue.get("SERVER_PORT")),
        reload=bool(envValue.get("SERVER_DEBUG_MODE")),
    )
