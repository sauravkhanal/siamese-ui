import numpy as np
import cv2
import os
from tqdm import tqdm
from preprocessing import preprocess_single_folder

def extract_signature_from_image(image_path,size = (300,300),margin = 15):
    image_name = (os.path.split(image_path))[1]
    image_name = image_name.split('.')[0]
    save_path = os.path.join(os.path.split(image_path)[0], f"extracted from {image_name}")
    if os.path.isdir(save_path) is False: #split at . to remove .png extension from folder name
        os.makedirs(save_path)
        #dir_made = True
    
    signature_grid = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)


    y_adj =0
    x_adj = 0
    rows = 7
    cols = 5
    xo,yo = (0,0)#top left corner ie: starting point
    x,y = (0,0)
    width = size[0] #width , x
    height = size[1] #height , y
    desired_size = size[0]#<----------------------------------------
    index = 1 #for incrementing name of image
    # dir_made = False
    # adj = 0 # in order to adjust

    for i in range(rows):
        for j in range(cols):

            cropped_image = signature_grid[y + margin: y - margin + height, x + margin: x - margin + width]

            # crop rectangle part only
            #gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            gray = cropped_image.copy()
            # To invert the text to white
            gray = 255*(gray < 128).astype(np.uint8)
            coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
            # Find minimum spanning bounding box
            xa, ya, wa, ha = cv2.boundingRect(coords)
            # Crop the image - note we do this on the original image
            rect = cropped_image[ya:ya+ha, xa:xa+wa]

            # now add paddinga and make square
            var = rect.shape
            old_size = var[:2]
            ratio = float(desired_size)/max(old_size)
            new_size = tuple([int(xa*ratio) for xa in old_size])
            im = cv2.resize(rect, (new_size[1], new_size[0]))
            delta_w = desired_size - new_size[1]
            delta_h = desired_size - new_size[0]
            top, bottom = delta_h//2, delta_h-(delta_h//2)
            left, right = delta_w//2, delta_w-(delta_w//2)
            color = [255, 255, 255]
            new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

            cv2.imwrite(f'{save_path}/sign{index}.png',new_im)
            x = x + width #next gird in same row
            index+=1 #increment for namea

        x = xo #reset x to the leftmost border

        y = y + height #increment y to next row
    preprocess_single_folder(save_path,save_path)
    # print("Execution completed")
    # if dir_made is True:
    #     print(f'New directory made : {folder_name}')
    # else:
    #     print(f'Directory found, files replaced : {folder_name}')

def extract_signature_from_directory(dir_path,size = (200,200),margin = 5):
    image_list = os.listdir(dir_path)
    image_list = [x for x in image_list if x.endswith('png') or x.endswith('PNG') or x.endswith('jpg') or x.endswith('JPG')]
    for image_name in tqdm(image_list):
        extract_signature_from_image(os.path.join(dir_path,image_name), size = size, margin = margin)