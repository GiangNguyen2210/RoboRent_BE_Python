import base64
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis


# Load model 1 lần duy nhất
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640, 640))


def decode_base64_image(base64_str: str):
    header, encoded = base64_str.split(",") if "," in base64_str else ("", base64_str)
    img_data = base64.b64decode(encoded)
    np_data = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    return img


def extract_embedding(image):
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
