import cv2
import os
from tqdm import tqdm

def resize_directory(directory,size=(1100,1540)):
    image_name_list = os.listdir(directory)
    for image_name in tqdm(image_name_list):
        image_path = os.path.join(directory,image_name)
        image = cv2.imread(os.path.join(image_path))
        image = cv2.resize(image,size)
        cv2.imwrite(image_path,image)

def resize_image(image_path, size=(1100,1540)):
    image = cv2.imread(image_path)
    image = cv2.resize(image,size)
    cv2.imwrite(image_path,image)
