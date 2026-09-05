import time
# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import numpy as np

class AIInferenceEngine:
    def __init__(self, model_ai1_path=None, model_ai2_path=None, model_ai3_path=None):
        print("AI Inference Engine khoi tao.")
    
    def run_ai_1(self, image):
        time.sleep(0.03)
        annotated = image.copy()
        is_ok = True
        cv2.putText(annotated, "AI1: OK", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,255,0), 4)
        return is_ok, "AI1_OK", annotated
    
    def run_ai_2(self, image):
        time.sleep(0.03)
        annotated = image.copy()
        is_ok = True
        cv2.putText(annotated, "AI2: OK", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        return is_ok, "AI2_OK", annotated
    
    def run_ai_3(self, image):
        time.sleep(0.03)
        annotated = image.copy()
        is_ok = True
        cv2.putText(annotated, "AI3: OK", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        return is_ok, "AI3_OK", annotated