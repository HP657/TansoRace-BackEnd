import random
from Modules.Module_Basic import *


class controllerAuth_Login(BaseModel):
    user_id: str
    user_pw: str


class controllerAuth_Register(BaseModel):
    user_id: str
    role_type: str = "company"
    user_pw: str
    user_name: str
    user_type: str = "이사진"
    user_role: str
    user_code: str = str(random.randint(100000, 99999999))
