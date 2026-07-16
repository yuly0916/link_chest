from dotenv import load_dotenv
from starlette.responses import RedirectResponse

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.category_router import category
from router.login_router import login
from router.link_router import link
import uvicorn

app = FastAPI()
app.include_router(login)
app.include_router(link)
app.include_router(category)

app.add_middleware(
    CORSMiddleware,
    # allow_origins = ["http://43.203.122.72/"],
    allow_origins = ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)