'''
@saurav
takes filename of scanned paper full of signature
width and height are the size of squares 
by default margin is 5 to remove inconsistency around border area
thus if input is 200*200 then signature images are of size 190*190
!!!!!!!!!!!!the file name shouldnot have space and mustnot begin with number!!!!!!!!!!!!!!!
'''

from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter as tk

import numpy as np
import cv2
import os
# import image_browser


# def open_img():
#     # Select the Imagename  from a folder
#     x = openfilename()
#     print(x)
#     # opens the image
#     img = Image.open(x)

#     # resize the image and apply a high-quality down sampling filter
#     img = img.resize((250, 250), Image.ANTIALIAS)

#     # PhotoImage class is used to add image to widgets, icons etc
#     img = ImageTk.PhotoImage(img)

#     # create a label
#     panel = Label(root0, image=img)

#     # set the image as img
#     panel.image = img
#     panel.grid(row=2)

def image_crop():
    def openfilename():
        filename = filedialog.askopenfilename(title='open image to crop')
        return filename

    def directory():
        root = tk.Tk()
        root.withdraw()
        dirname = filedialog.askdirectory(
            parent=root, initialdir="/", title='Please select a directory to save')
        return dirname

    filepath = openfilename()
    # folder_name = input(
    #     "enter name of folder to save the images eg(E:/MINOR PROJECT/CODE): ")
    folder_name = directory()

    if os.path.isdir(f'{folder_name}') is False:
        os.makedirs(f'{folder_name}')
        dir_made = True

    signature_gird = cv2.imread(f'{filepath}', cv2.IMREAD_GRAYSCALE)
    rows = 7
    cols = 6
    xo, yo = (0, 0)  # top left corner ie: starting point
    x, y = (0, 0)
    width = 200  # width , x
    height = 200  # height , y
    desired_size = 200  # <----------------------------------------
    index = 1  # for incrementing name of image
    margin = 3
    dir_made = False
    adj = 0  # in order to adjust

    for i in range(rows):
        for j in range(cols):

            cropped_image = signature_gird[y + margin: y -
                                           margin + height, x + margin: x - margin + width]

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
            new_im = cv2.copyMakeBorder(
                im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

            cv2.imwrite(f'{folder_name}/sign{index}.png', new_im)
            x = x + width  # next gird in same row
            index += 1  # increment for namea

        x = xo  # reset x to the leftmost border

        y = y + height  # increment y to next row

    print("Execution completed")
    if dir_made is True:
        print(f'New directory made : {folder_name}')
    else:
        print(f'Directory found, files replaced : {folder_name}')
