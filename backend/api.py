from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.user import router as user_router
from backend.routes.auth import router as auth_router
from backend.routes.address import router as address_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix='/users', tags=['users'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(address_router, prefix='/address', tags=['address'])


@app.get("/")
def main():
    return {"message": "Hello World"}

