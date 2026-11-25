
import cv2
from ultralytics import YOLO
from pathlib import Path

# Locate trained model
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "runs" / "product_classifier" / "weights" / "best.pt"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

print("Loading AI model...")
model = YOLO(str(MODEL_PATH))
print("Model loaded successfully!")

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Camera could not be opened!")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("Camera started! Press Q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    # Predict product
    results = model.predict(
        source=frame,
        imgsz=224,
        verbose=False
    )

    result = results[0]
    class_id = result.probs.top1
    confidence = float(result.probs.top1conf)
    product = model.names[class_id]

    # Display prediction
    label = f"{product} | {confidence * 100:.1f}%"

    cv2.rectangle(frame, (10, 10), (630, 85), (20, 20, 20), -1)
    cv2.putText(
        frame, label, (25, 58),
        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
        (0, 255, 100), 2
    )

    cv2.imshow("AI Product Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
