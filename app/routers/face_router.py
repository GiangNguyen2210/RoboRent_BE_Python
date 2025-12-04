from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.face_schema import (
    FaceProfileCreateRequest,
    FaceVerificationRequest,
    FaceVerificationResponse
)
from app.services.face_service import FaceService

router = APIRouter(prefix="/face", tags=["Biometric Face Recognition"])


# ---------------------------------------------------------
# 1. Register Face Profile
# ---------------------------------------------------------
@router.post("/profile/create")
def create_profile(req: FaceProfileCreateRequest, db: Session = Depends(get_db)):
    profile = FaceService.create_face_profile(
        db,
        req.account_id,
        req.citizen_id,
        req.image_base64
    )

    if profile is None:
        raise HTTPException(status_code=400, detail="Không tìm thấy khuôn mặt trong ảnh")

    return {
        "message": "Face profile created successfully",
        "profile_id": profile.Id
    }


# ---------------------------------------------------------
# 2. Verify face
# ---------------------------------------------------------
@router.post("/verify", response_model=FaceVerificationResponse)
def verify_face(req: FaceVerificationRequest, db: Session = Depends(get_db)):
    result = FaceService.verify_face(
        db,
        req.account_id,
        req.image_base64,
    )
    return result

@router.post("/face/profile/create-from-cccd")
def create_profile_from_cccd(req: FaceProfileCreateRequest, db: Session = Depends(get_db)):

    profile, error = FaceService.create_from_cccd(
        db,
        req.account_id,
        req.citizen_id,
        req.image_base64
    )

    if error:
        raise HTTPException(status_code=400, detail=error)

    return {
        "message": "Face profile từ CCCD đã được tạo",
        "profile_id": profile.Id
    }
