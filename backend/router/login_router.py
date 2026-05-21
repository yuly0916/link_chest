from fastapi import APIRouter
import requests
from entity.models import User
from sqlmodel import select
from sqlalchemy.exc import NoResultFound
from jose import jwt, JWTError
import datetime
from starlette.responses import RedirectResponse
from db import SessionDep
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import os

login = APIRouter()
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
LOGIN_SUCCESS_PAGE = os.environ.get('LOGIN_SUCCESS_PAGE')


def create_token(user_code, name, profile_img, kakao_user_id):
    """
    티켓 발행 하는 함수
    """
    payload = {
        "user_code": user_code,
        "name": name,
        "profile_img": profile_img,
        "kakao_user_id": kakao_user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@login.get("/login/redirect")
def kakao_login_redirect(session:SessionDep, code: str | None = None, error: str | None=None, error_description:str|None=None):
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post("https://kauth.kakao.com/oauth/token",data)
    kakao_response_data = response.json()
    headers = {
        "Authorization": f"Bearer {kakao_response_data['access_token']}",
        "Content_Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    response2 = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    user_infor = response2.json()
    user_detail = user_infor["properties"]
    user = User(user_code=None, name=user_detail["nickname"], profile_image=user_detail["profile_image"], email=None, kakao_user_id=user_infor["id"])
    sql = select(User).where(User.kakao_user_id==user_infor["id"])
    try:
        result = session.exec(sql).one()
        # 로그인
    except NoResultFound:
        session.add(user)
        session.commit()

    sql = select(User).where(User.kakao_user_id==user_infor["id"])
    result = session.exec(sql).first().dict()
    token = create_token(result["user_code"], result["name"], result["profile_image"], result["kakao_user_id"])

    res = RedirectResponse(url=LOGIN_SUCCESS_PAGE)
    res.set_cookie(key="jwt_token", value=token)
    return res

@login.get("/home")
def home_page():
    return {"status":"success","message":"성공"}