import os
import cv2
import numpy as np
from tqdm import tqdm
from pathlib import Path

def preprocess_single_folder(folder_path,save_folder_path, final_img_size = (200,200), power_law=False, segment=True, log_transform=False):
  image_batch = os.listdir(folder_path)
  image_data = [x for x in image_batch if x.endswith('png') or x.endswith('PNG') or x.endswith('jpg') or x.endswith('JPG')]

  for sample in tqdm(image_data):
    img_path = os.path.join(folder_path, sample)
    #importing images from drive
    #x = image.load_img(img_path)
    #img = image.img_to_array(x)
    img = cv2.imread(img_path)
        
    #Perfom Median blur on image
    mbvalue = int(np.max(img.shape)/200)
    mbvalue = mbvalue if mbvalue%2==1 else mbvalue+1
    img = cv2.medianBlur(img, mbvalue)

    #changing RGB to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    #resize image to 600xH
    img = cv2.resize(img, (600, int(600*float(img.shape[0])/img.shape[1])))
    
    #if power_law enabled
    if(power_law):
      img = img**0.9
      img[img>255]=255
      img[img<0]=0
      img = img.astype('uint8')
          
    #denoising the grayscale image
    img = cv2.fastNlMeansDenoising(img, None, 10, 21)
    
    if (log_transform):
        img = (np.log(img+1)/(np.log(10+np.max(img))))*255
        img=img.astype('uint8')
    
    #Threshold binary image
    avg = np.average(img)
    _,image = cv2.threshold(img, int(avg)-30, 255, cv2.THRESH_BINARY)
            
    #segment the signature section only
    if(segment):
      seg = segmentImage(image)
      image = image[seg[2]:seg[3], seg[0]:seg[1]]
          
    #padding to make image into square
    lp, rp, tp, bp = (0,0,0,0)
    if(image.shape[0]>image.shape[1]):
      lp = int((image.shape[0]-image.shape[1])/2)
      rp = lp
    elif(image.shape[1]>image.shape[0]):
      tp = int((image.shape[1]-image.shape[0])/2)
      bp = tp
    image_padded = cv2.copyMakeBorder(image, tp, bp, lp, rp, cv2.BORDER_CONSTANT, value=255)

    #resizing the image
    img = cv2.resize(image_padded, final_img_size)

    #producing image negative
    img = 255-img

    #skeletonizing image
    #img = thin(img/255)

    #img = img.astype('bool')
    # cv2.imshow(sample,img)
    # cv2.waitKey(500)
    new_save_path = os.path.join(save_folder_path , sample)
    if not os.path.isdir(save_folder_path):
        os.makedirs(save_folder_path) 
    #print(str(new_save_path))
    cv2.imwrite(new_save_path, img)

def segmentImage(image):  
  hHist=np.zeros(shape=image.shape[0], dtype=int)
  vHist=np.zeros(shape=image.shape[1], dtype=int)

  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      if(image[i][j]==0):
        hHist[i]+=1
        vHist[j]+=1
  
  locLeft=0
  locRight=image.shape[0]
  locTop=0
  locBottom=image.shape[1]
  
  count=0
  for i in range(hHist.shape[0]):
    if(count<=0):
        count=0
        if(hHist[i]!=0):
            locTop=i
            count+=1
    else:
        if(hHist[i]!=0):
            count+=1
        else:
            count-=hHist.shape[0]/100

        if(count>hHist.shape[0]/30):
            break
            
  count=0
  for i in reversed(range(hHist.shape[0])):
    if(count<=0):
        count=0
        if(hHist[i]!=0):
            locBottom=i
            count+=1
    else:
        if(hHist[i]!=0):
            count+=1
        else:
            count-=hHist.shape[0]/100

        if(count>hHist.shape[0]/30):
            break
            
  count=0
  for i in range(vHist.shape[0]):
    if(count<=0):
        count=0
        if(vHist[i]!=0):
            locLeft=i
            count+=1
    else:
        if(vHist[i]!=0):
            count+=1
        else:
            count-=vHist.shape[0]/100

        if(count>vHist.shape[0]/30):
            break
            
  count=0
  for i in reversed(range(vHist.shape[0])):
    if(count<=0):
        count=0
        if(vHist[i]!=0):
            locRight=i
            count+=1
    else:
        if(vHist[i]!=0):
            count+=1
        else:
            count-=vHist.shape[0]/100

        if(count>vHist.shape[0]/30):
            break
            
  return locLeft, locRight, locTop, locBottom

def preprocess_multiple_folder(folder_path, final_img_size = (200,200), power_law=False, segment=True, log_transform=False): 
    list_of_dirs = os.listdir(folder_path)
    print("TOTAL NUMBER OF DIRECTORIES : " + str(len(list_of_dirs)) )
    for index,dirs in enumerate(list_of_dirs):
        print("Processing directory " + str(index)+"/"+str(len(list_of_dirs)))
        path = os.path.join(folder_path, dirs)
        preprocess_single_folder(folder_path=path, save_folder_path=path, final_img_size = final_img_size, power_law=power_law, segment=segment, log_transform=log_transform)

def preprocess_single_image(image_path,save_path, final_img_size = (200,200), power_law=False, segment=True, log_transform=False):
    img = cv2.imread(image_path)
        
    #Perfom Median blur on image
    mbvalue = int(np.max(img.shape)/200)
    mbvalue = mbvalue if mbvalue%2==1 else mbvalue+1
    img = cv2.medianBlur(img, mbvalue)

    #changing RGB to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    #resize image to 600xH
    img = cv2.resize(img, (600, int(600*float(img.shape[0])/img.shape[1])))
    
    #if power_law enabled
    if(power_law):
      img = img**0.9
      img[img>255]=255
      img[img<0]=0
      img = img.astype('uint8')
          
    #denoising the grayscale image
    img = cv2.fastNlMeansDenoising(img, None, 10, 21)
    
    if (log_transform):
        img = (np.log(img+1)/(np.log(10+np.max(img))))*255
        img=img.astype('uint8')
    
    #Threshold binary image
    avg = np.average(img)
    _,image = cv2.threshold(img, int(avg)-30, 255, cv2.THRESH_BINARY)
            
    #segment the signature section only
    if(segment):
      seg = segmentImage(image)
      image = image[seg[2]:seg[3], seg[0]:seg[1]]
          
    #padding to make image into square
    lp, rp, tp, bp = (0,0,0,0)
    if(image.shape[0]>image.shape[1]):
      lp = int((image.shape[0]-image.shape[1])/2)
      rp = lp
    elif(image.shape[1]>image.shape[0]):
      tp = int((image.shape[1]-image.shape[0])/2)
      bp = tp
    image_padded = cv2.copyMakeBorder(image, tp, bp, lp, rp, cv2.BORDER_CONSTANT, value=255)

    #resizing the image
    img = cv2.resize(image_padded, final_img_size)

    #producing image negative
    img = 255-img

    if not os.path.isdir(save_path):
        os.makedirs(save_path) 

    temp = image_path.split('/')

    new_save_path = os.path.join(save_path,temp[-1])

    #print(str(new_save_path))
    cv2.imwrite(new_save_path, img)


