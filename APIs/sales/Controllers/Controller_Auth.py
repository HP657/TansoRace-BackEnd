from Modules.Module_Basic import *


class controllerAuth_Login(BaseModel):
    user_id: str
    user_pw: str


class controllerAuth_Register(BaseModel):
    user_id: str
    role_type: str = "sales"
    user_pw: str
    user_name: str
    user_type: str
    user_role: str
    user_code: str
