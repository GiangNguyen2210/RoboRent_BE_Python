import os
os.environ["INSIGHTFACE_USE_TRT"] = "0"
os.environ["INSIGHTFACE_USE_CUDA"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # disable GPU

from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640, 640))
print("InsightFace model downloaded.")
