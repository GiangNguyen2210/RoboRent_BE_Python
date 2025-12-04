from pydantic import BaseModel


class FaceProfileCreateRequest(BaseModel):
    account_id: int
    citizen_id: str
    image_base64: str


class FaceVerificationRequest(BaseModel):
    account_id: int
    image_base64: str

class FaceVerificationResponse(BaseModel):
    success: bool
    match_score: float | None
    face_profile_id: int | None = None
