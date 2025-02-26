from Modules.Module_Basic import *


class controllerPoint_Set(BaseModel):
    point: int


class controllerPoint_Update(BaseModel):
    input_type: str = "add" or "remove"
    point: int