from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.get("/")
def list_accounts(db: Session = Depends(get_db)):
    return {
        "success": True,
        "data": db.query(models.Accounts).all()
    }
