from Modules.Module_Basic import *


class controllerQuestCount_Set(BaseModel):
    count: int


class controllerQuestCount_Update(BaseModel):
    input_type: str = "add" or "remove"
    count: int


class controllerQuest_Clear(BaseModel):
    quest_name: str