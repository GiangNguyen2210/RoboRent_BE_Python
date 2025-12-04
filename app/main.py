from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.accounts_router import router as accounts_router
from app.routers.face_router import router as face_router

app = FastAPI()

# Register routers
app.include_router(accounts_router)
app.include_router(face_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}
