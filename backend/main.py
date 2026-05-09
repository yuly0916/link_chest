from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.category_router import category
from router.login_router import login
from router.link_router import link


app = FastAPI()
app.include_router(login)
app.include_router(link)
app.include_router(category)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://43.203.122.72/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)