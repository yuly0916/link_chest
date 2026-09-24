from pydantic import BaseModel

class User(BaseModel):
    user_code:int
    name:str
    profile_img:str
    kakao_user_id:int
    login_type:int

class InforMessageDto(BaseModel):
    message: str