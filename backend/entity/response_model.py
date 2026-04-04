from pydantic import BaseModel


class LinkResponse(BaseModel):
    code: int
    title: str
    category_name: str
    link: str