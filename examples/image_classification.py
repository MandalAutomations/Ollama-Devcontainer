import os
from PIL import Image

def classify_image(image_path):
        return os.path.basename(image_path).split('.')[0]

def main():
    img_dir = os.path.join(os.path.dirname(__file__), 'img')
    if not os.path.isdir(img_dir):
        print(f"No image directory at {img_dir}. Drop .png/.jpg files there to classify.")
        return
    image_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for img_file in image_files:
        img_path = os.path.join(img_dir, img_file)
        image = Image.open(img_path)
        label = classify_image(img_path)
        print(f"Image: {img_file} -> Predicted label: {label}")

if __name__ == "__main__":
    main()