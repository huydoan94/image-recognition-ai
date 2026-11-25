from pathlib import Path
import random, shutil
from ultralytics import YOLO
from labels import PRODUCTS

ROOT = Path(__file__).resolve().parents[1]
RAW, DATA = ROOT/"raw_images", ROOT/"dataset"

def main():
    if DATA.exists():
        shutil.rmtree(DATA)
    random.seed(42)
    for _, name, folder in PRODUCTS:
        images = list((RAW/folder).glob("*.jpg"))
        if len(images) < 10:
            print(f"{name}: only {len(images)} photos. Capture at least 10; aim for 30-50.")
            return
        random.shuffle(images)
        nval = max(2, int(len(images)*.2))
        for split, group in (("train", images[nval:]), ("val", images[:nval])):
            dest = DATA/split/folder
            dest.mkdir(parents=True, exist_ok=True)
            for i, img in enumerate(group):
                shutil.copy2(img, dest/f"{i:04d}.jpg")
        print(f"{name}: {len(images)-nval} train, {nval} validation")
    print("Loading small YOLO11n classification model. First run downloads weights.")
    model = YOLO("yolo11n-cls.pt")
    model.train(data=str(DATA), epochs=20, imgsz=160, batch=16,
                device="cpu", workers=0, patience=5,
                project=str(ROOT/"runs"), name="product_classifier", exist_ok=True)
    print("Training complete. Run src\\recognize.py")

if __name__ == "__main__":
    main()
