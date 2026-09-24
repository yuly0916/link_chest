from typing import Iterator

from fastapi import APIRouter, Depends, Body, HTTPException
from router.login_router import get_current_user
from db import SessionDep
from sqlmodel import select, or_
from entity.models import Category

category = APIRouter(dependencies=[Depends(get_current_user)])

@category.get("/category",responses={401:{"description":"Invalid token"}})
def get_user_category(session: SessionDep, user=Depends(get_current_user)):
    if "login_type" not in user:
        raise HTTPException(status_code=401, detail="Invalid token")

    if user["login_type"] == 0:
        return []
    sql = select(Category).where(or_(Category.user_code == user["user_code"]))
    result = session.exec(sql).all()
    return result

@category.post("/category", responses={409:{"description":"이미 존재하는 카테고리입니다."}})
def create_category( session:SessionDep, user=Depends(get_current_user), name:str = Body(...)):
    if user["login_type"] == 0:
        return 0

    r:Category = session.scalar(select(Category).where(Category.name==name, Category.user_code==user["user_code"]))
    if r is None:
        category = Category(user_code=user["user_code"], name=name)
        session.add(category)
        session.commit()
        r:Category = session.scalar(select(Category).where(Category.name==name, Category.user_code==user["user_code"]))
        return r.category_code
    else:
        raise HTTPException(status_code=409, detail="이미 존재하는 카테고리입니다.")

