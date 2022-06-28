from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.user import router as user_router
from backend.routes.auth import router as auth_router
from backend.routes.role import router as role_router
from backend.routes.group import router as group_router

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
app.include_router(role_router, prefix='/role', tags=['role'])
app.include_router(group_router, prefix='/group', tags=['group'])


@app.get("/")
def main():
    return {"message": "Hello World"}

