from fastapi import APIRouter, Depends
from db import SessionDep
from entity.response_model import LinkResponse
from router.login_router import get_current_user
from sqlmodel import select, desc, asc, delete
from entity.models import Link, Category
link = APIRouter(dependencies=[Depends(get_current_user)])
from typing import Iterable

@link.get("/link_check")
def check_link(session:SessionDep, user=Depends(get_current_user)):
    sql = select(Link).where(Link.user_code == user["user_code"])
    result = session.exec(sql).all()
    if len(result) == 0:
        return False
    else:
        return True

@link.post("/link")
def create_link(link: Link, session:SessionDep, user=Depends(get_current_user)):
    try:
        print(link)
        link.user_code = user["user_code"]
        session.add(link)
        session.commit()
        return True
    except:

        return False


@link.get("/link")
def get_link(sort: bool, session: SessionDep, user=Depends(get_current_user)):
    print(sort)
    sql = select(Link).where(Link.user_code == user["user_code"])
    sql = sql.order_by(desc(Link.created_at)) if sort else sql.order_by(asc(Link.created_at))

    results: Iterable[Link] = session.scalars(sql)
    res = []
    for r in results:
        print(r)
        res.append(LinkResponse(code=r.link_code, title=r.title, category_name=r.category.name, link=r.link))
    return res

@link.get("/link/category")
def get_link_category(name: str, session:SessionDep, user=Depends(get_current_user)):
    sql = select(Link).join(Category).where(Link.user_code==user["user_code"], Category.name==name)
    result: Iterable[Link] = session.scalars(sql)
    res = []
    for r in result:
        res.append(LinkResponse(code=r.link_code, title=r.title, category_name=r.category.name, link=r.link))
    return res

@link.delete("/content")
def delete_content(code: int, session:SessionDep, user=Depends(get_current_user)):
    sql = delete(Link).where(code == Link.link_code)
    session.exec(sql)
    session.commit()


