from typing import Iterator

from fastapi import APIRouter, Depends, Body, HTTPException
from router.login_router import get_current_user
from db import SessionDep
from sqlmodel import select, or_
from entity.models import Category

category = APIRouter(dependencies=[Depends(get_current_user)])

@category.get("/category")
def get_user_category(session: SessionDep, user=Depends(get_current_user)):
    sql = select(Category).where(or_(Category.user_code == user["user_code"]))
    result = session.exec(sql).all()
    return result

@category.post("/category")
def create_category( session:SessionDep, user=Depends(get_current_user), name:str = Body(...)):
    r:Category = session.scalar(select(Category).where(Category.name==name, Category.user_code==user["user_code"]))
    print(r)
    if r is None:
        category = Category(user_code=user["user_code"], name=name)
        session.add(category)
        session.commit()
        r:Category = session.scalar(select(Category).where(Category.name==name, Category.user_code==user["user_code"]))
        return r.category_code
    else:
        raise HTTPException(status_code=409, detail="이미 존재하는 카테고리에요.")

