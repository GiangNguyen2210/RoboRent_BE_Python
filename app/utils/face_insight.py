import base64
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

# Lazy-loaded model
import threading

_face_model = None
_face_lock = threading.Lock()

def get_face_model():
    global _face_model
    if _face_model is None:
        with _face_lock:
            if _face_model is None:
                from insightface.app import FaceAnalysis
                model = FaceAnalysis(
                    name="buffalo_l",
                    providers=["CPUExecutionProvider"]
                )
                model.prepare(ctx_id=0, det_size=(640, 640))
                _face_model = model
    return _face_model

# def decode_base64_image(base64_str: str):
#     header, encoded = base64_str.split(",") if "," in base64_str else ("", base64_str)
#     img_data = base64.b64decode(encoded)
#     np_data = np.frombuffer(img_data, np.uint8)
#     img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
#     return img
def decode_base64_image(base64_str: str):
    try:
        # Remove the header if present
        if "," in base64_str:
            _, base64_str = base64_str.split(",", 1)

        # Fix missing padding (base64 length must be divisible by 4)
        base64_str += "=" * (-len(base64_str) % 4)

        # Decode base64
        img_data = base64.b64decode(base64_str)
        np_data = np.frombuffer(img_data, np.uint8)

        # Decode to OpenCV image
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        return img

    except Exception as e:
        print("BASE64 DECODE ERROR:", e)
        return None

def extract_embedding(image):
    app = get_face_model()      # lazy loaded
    faces = app.get(image)

    if len(faces) == 0:
        return None
    return faces[0].embedding.tolist()


def compare_embeddings(emb1, emb2, threshold=0.45):
    """Cosine distance, threshold tùy InsightFace"""
    emb1 = np.array(emb1)
    emb2 = np.array(emb2)

    # cosine similarity: 1 = giống y hệt, -1 = khác hoàn toàn
    cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    return float(cos_sim), cos_sim >= threshold
