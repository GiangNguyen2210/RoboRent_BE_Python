import easyocr
import re
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.models import FaceProfiles, FaceVerifications
from app.utils.face_insight import decode_base64_image, extract_embedding, compare_embeddings
import json
import hashlib

THRESHOLD = 0.45

ocr_reader = easyocr.Reader(['vi', 'en'], gpu=False)

class FaceService:

    @staticmethod
    def create_from_cccd(db: Session, account_id: int, citizen_id: str, base64_img: str):

        # 1) Decode image
        img = decode_base64_image(base64_img)
        if img is None:
            return None, "Ảnh CCCD không hợp lệ"

        # 2) OCR extract text
        results = ocr_reader.readtext(img, detail=0)
        ocr_text = " ".join(results).lower()

        print("\n================ OCR DEBUG OUTPUT ================")
        print("RAW OCR RESULTS:")
        print(results)
        print("\nJOINED OCR TEXT:")
        print(ocr_text)
        print("=================================================\n")

        # --- CCCD VALIDATION ---
        if "căn cước công dân" not in ocr_text:
            return None, "Ảnh không phải là mặt trước thẻ CCCD"

        # Extract CCCD number
        match = re.search(r"\b\d{12}\b", ocr_text)
        if not match:
            return None, "Không tìm thấy số CCCD trong ảnh"

        ocr_id_number = match.group()

        if ocr_id_number != citizen_id:
            return None, f"Số CCCD không khớp (ảnh: {ocr_id_number}, nhập: {citizen_id})"

        # 3) Extract face embedding
        embedding = extract_embedding(img)
        if embedding is None:
            return None, "Không tìm thấy khuôn mặt trong ảnh CCCD"

        embedding_json = json.dumps(embedding)
        hash_sha256 = hashlib.sha256(embedding_json.encode("utf-8")).hexdigest()

        # ------------------------------------------------------------
        # 🔥 CHECK IF PROFILE ALREADY EXISTS FOR THIS ACCOUNT
        # ------------------------------------------------------------
        existing_profile = (
            db.query(FaceProfiles)
            .filter(FaceProfiles.AccountId == account_id)
            .first()
        )

        if existing_profile:
            # UPDATE EXISTING PROFILE
            existing_profile.CitizenId = citizen_id
            existing_profile.Embedding = embedding_json
            existing_profile.HashSha256 = hash_sha256
            existing_profile.Model = "insightface-buffalo_l"
            existing_profile.IsActive = True
            existing_profile.LastUsedAt = datetime.utcnow()

            db.commit()
            db.refresh(existing_profile)

            return existing_profile, None

        # ------------------------------------------------------------
        # 🔥 OTHERWISE CREATE NEW PROFILE
        # ------------------------------------------------------------
        new_profile = FaceProfiles(
            AccountId=account_id,
            CitizenId=citizen_id,
            Embedding=embedding_json,
            Model="insightface-buffalo_l",
            HashSha256=hash_sha256,
            CreatedAt=datetime.utcnow(),
            IsActive=True,
            FrontIdImagePath=None,
            LastUsedAt=None
        )

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        return new_profile, None

    # ---------------------------------------------------------
    # CREATE PROFILE — đăng ký gương mặt từ CCCD
    # ---------------------------------------------------------
    @staticmethod
    def create_face_profile(db: Session, account_id: int, citizen_id: str, base64_image: str):
        img = decode_base64_image(base64_image)
        embedding = extract_embedding(img)

        if embedding is None:
            return None

        profile = FaceProfiles(
            CitizenId=citizen_id,
            Embedding=embedding,
            Model="insightface-buffalo_l",
            HashSha256="",  # optional
            CreatedAt=datetime.utcnow(),
            IsActive=True,
            AccountId=account_id,
            FrontIdImagePath=None,
            LastUsedAt=None
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile

    # ---------------------------------------------------------
    # VERIFY FACE — xác thực sinh trắc học
    # ---------------------------------------------------------
    @staticmethod
    def verify_face(db: Session, account_id: int, base64_image: str | None):
        img = decode_base64_image(base64_image)
        embedding = extract_embedding(img)

        if embedding is None:
            return {
                "success": False,
                "match_score": None,
            }

        # Lấy profile đã đăng ký
        profile = (
            db.query(FaceProfiles)
            .filter(FaceProfiles.AccountId == account_id, FaceProfiles.IsActive == True)
            .first()
        )

        if not profile:
            return {
                "success": False,
                "match_score": None,
            }

        # # So sánh embedding
        # match_score, is_match = compare_embeddings(embedding, profile.Embedding, threshold=THRESHOLD)
        # Convert DB string -> list float
        db_embedding = json.loads(profile.Embedding)

        match_score, is_match = compare_embeddings(
        embedding,
        db_embedding,
        threshold=THRESHOLD
        )


        # Log verification
        verification = FaceVerifications(
            Threshold=THRESHOLD,
            Result="Success" if is_match else "Failed",
            VerifiedAt=datetime.utcnow(),
            AccountId=account_id,
            FaceProfileId=profile.Id,
            MatchScore=match_score,
        )

        db.add(verification)
        db.commit()

        return {
            "success": is_match,
            "match_score": match_score,
            "face_profile_id": profile.Id
        }
