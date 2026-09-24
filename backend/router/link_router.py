from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from db import SessionDep
from entity.response_model import LinkResponse
from router.login_router import get_current_user
from sqlmodel import select, desc, asc, delete
from entity.models import Link, Category
link = APIRouter(dependencies=[Depends(get_current_user)])
from typing import Iterable

@link.get("/link_check", responses={500:{"description":"링크 존재 확인 중 오류 발생했습니다."},401:{"description":"Invalid token"}})
def check_link(session:SessionDep, user=Depends(get_current_user)):
    try:
        if user["login_type"] == 0:
            return True
        sql = select(Link).where(Link.user_code == user["user_code"])
        result = session.exec(sql).all()
        if len(result) == 0:
            return False
        else:
            return True
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="링크 존재 확인 중 오류 발생했습니다."
        )
    except KeyError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

@link.post("/link", responses={401:{"description":"Invalid token"},500:{"description":"링크 존재 확인 중 오류 발생했습니다."}})
def create_link(link: Link, session:SessionDep, user=Depends(get_current_user)):
    try:
        if user["login_type"] == 0:
            return True
        link.user_code = user["user_code"]
        session.add(link)
        session.commit()
        return True
    except KeyError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500, detail="링크를 등록하는 중 오류 발생했습니다."
        )




@link.get("/link",responses={401:{"description":"Invalid token"},500:{"description":"링크 또는 연결된 카테고리 정보를 읽을 수 없습니다."}})
def get_link(sort: bool, session: SessionDep, user=Depends(get_current_user)):
    try:
        sql = select(Link).where(Link.user_code == user["user_code"])
        sql = sql.order_by(desc(Link.created_at)) if sort else sql.order_by(asc(Link.created_at))

        results: Iterable[Link] = session.scalars(sql)
        res = []
        for r in results:
            res.append(LinkResponse(code=r.link_code, title=r.title, category_name=r.category.name, link=r.link))
        return res
    except AttributeError:
        raise HTTPException(
            status_code=500, detail="링크 또는 연결된 카테고리 정보를 읽을 수 없습니다."
        )
    except KeyError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

@link.get("/link/category",responses={401:{"description":"Invalid token"},500:{"description":"카테고리별 링크를 조회하는 중 오류가 발생했습니다."}})
def get_link_category(name: str, session:SessionDep, user=Depends(get_current_user)):
    try:
        sql = select(Link).join(Category).where(Link.user_code==user["user_code"], Category.name==name)
        result: Iterable[Link] = session.scalars(sql)
        res = []
        for r in result:
            res.append(LinkResponse(code=r.link_code, title=r.title, category_name=r.category.name, link=r.link))
        return res
    except KeyError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="카테고리별 링크를 조회하는 중 오류가 발생했습니다."
        )

@link.delete("/content",responses={500:{"description":"링크를 삭제하는 중 오류가 발생했습니다."}})
def delete_content(code: int, session:SessionDep, user=Depends(get_current_user)):
    try:
        sql = delete(Link).where(code == Link.link_code)
        session.exec(sql)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="링크를 삭제하는 중 오류가 발생했습니다."
        )


