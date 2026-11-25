# Image recognition AI

Recognise 13 everyday products from a webcam. You take photos of your own items, train a small image classifier on them, and then point the webcam at a product to see its name and a confidence score.

It runs on Windows with Python and works on a CPU. You don't need a GPU.

## Products

| Key | Product     | Key | Product   |
| --- | ----------- | --- | --------- |
| A   | Phone       | H   | Snacks    |
| B   | Charger     | I   | Notebook  |
| C   | Bangle      | J   | Pen       |
| D   | Body Lotion | K   | Glue      |
| E   | Lipgloss    | L   | Cup       |
| F   | Spoon       | M   | Bottle    |
| G   | Bournvita   |     |           |

The list is in [src/labels.py](src/labels.py). The key is the one you press to choose that product when you take photos.

## How it works

1. **Collect** ([src/collect_data.py](src/collect_data.py)): saves the area inside a green square on the webcam picture to `raw_images/<product>/`.
2. **Train** ([src/train_model.py](src/train_model.py)): splits the photos 80/20 into `dataset/train` and `dataset/val`, then fine-tunes the YOLO11n classification model (`yolo11n-cls.pt`) at 160 px for up to 20 epochs on the CPU. The trained model is saved to `runs/product_classifier/weights/best.pt`.
3. **Recognise** ([src/recognize.py](src/recognize.py)): classifies each webcam frame and shows the most likely product and its confidence.

## Requirements

- Windows with a webcam
- Python 3.11, 3.12 or 3.13, with the `py` launcher
- An internet connection the first time you train, to download the YOLO11n weights

## Setup

Double-click `setup.bat`, or run it from a terminal:

```powershell
.\setup.bat
```

It creates a `.venv` virtual environment and installs [Ultralytics](https://docs.ultralytics.com/) and OpenCV.

To set it up by hand:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install ultralytics opencv-python
```

## Usage

### 1. Collect photos

```powershell
.\.venv\Scripts\python.exe src\collect_data.py
```

- Press a letter from **A** to **M** to choose a product.
- Put the product inside the green square and press **Space** to save a photo.
- Press **Q** to quit.

The number of photos saved for each product is shown along the top of the window. Each product needs at least **10** photos before you can train, and 30–50 is better. Change the angle, distance, background and lighting between photos.

### 2. Train

```powershell
.\.venv\Scripts\python.exe src\train_model.py
```

Training takes a few minutes on a CPU. Each run deletes and rebuilds `dataset/` from `raw_images/`, and replaces the model you trained before.

### 3. Recognise live

```powershell
.\run.bat
```

You can also double-click `run.bat`, or run `.\.venv\Scripts\python.exe src\recognize.py`. If you haven't trained a model yet, `run.bat` tells you so.

Hold one product in front of the camera so that it fills most of the picture. The model classifies the whole frame, not just a box. Press **Q** to quit.

## Tips

- Use bright, even light, and keep the product centred and large in the picture.
- If two products get mixed up, take more varied photos of both and train again.
- The model always picks one of the 13 products, even when none of them is in view. The confidence shows how sure it is, but even a high score can be wrong.
- If the camera won't open, close other apps that use it. If you have more than one camera, change `CAMERA_INDEX` in `collect_data.py`, or the `0` in `cv2.VideoCapture(0)` in `recognize.py`.

## Legacy YOLO-World detector

[src/product_detector.py](src/product_detector.py) is the earlier version. It uses the YOLO-World model (`yolov8s-worldv2.pt`) to look for products from text descriptions and needs no training, but it is slower and less reliable for your own items. To try it:

```powershell
.\.venv\Scripts\python.exe src\product_detector.py
```

## Project layout

```text
src/
  labels.py            product list (keys, names, folder names)
  collect_data.py      take training photos from the webcam
  train_model.py       build the dataset and train the classifier
  recognize.py         live recognition with the trained model
  product_detector.py  legacy YOLO-World detector
setup.bat              create .venv and install dependencies
run.bat                start live recognition
requirements.txt
```

These folders are created as you go and are not committed to git (see `.gitignore`): `raw_images/`, `dataset/`, `runs/` and `.venv/`. Your own photos stay on your computer.
