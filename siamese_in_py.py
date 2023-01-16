import os
import cv2
from PIL import Image
import numpy as np

#image_directory = "A:/signatures/" #prompt to select image directory
SIZE = 50
image_size = (SIZE,SIZE)

'''
donot delete
error may occur on make_dataset while doing list1+list2
the error doesnt occur while running make_dataset but it mismatches the images and labels
thus resulting in error while training data 
this needs to get considered upon getting lower accuracy value
-saurav
'''
def make_train_dataset (image_dir1:str, image_dir2:str)->list:
    '''
    path must have / at end 
    to be sorted at final
    '''
    dataset = []
    label = []
    #image_dir = input("PROMPT TO select image directory")
    images = os.listdir(image_dir1)
    for i,image_name in enumerate(images):
        if (image_name.split('.')[1] == 'png'):
            image = cv2.imread(os.path.join(image_dir1,image_name), cv2.COLOR_BGR2GRAY)
            image = Image.fromarray(image)
            if(image.height != image_size[0] and image.width != image_size[1]):
                image = image.resize((SIZE, SIZE))
            dataset.append(np.array(image))
            label.append(0)
    
    images = os.listdir(image_dir2)
    for i,image_name in enumerate(images):
        if (image_name.split('.')[1] == 'png'):
            image = cv2.imread(os.path.join(image_dir2,image_name), cv2.COLOR_BGR2GRAY)
            image = Image.fromarray(image)
            image = image.resize((SIZE, SIZE))
            dataset.append(np.array(image))
            label.append(1)

    return dataset,label #needs to be converted into numpy array

import itertools

def make_paired_dataset(X, y):
  X_pairs, y_pairs = [], []

  tuples = [(x1, y1) for x1, y1 in zip(X, y)]
  
  for t in itertools.product(tuples, tuples):
    pair_A, pair_B = t
    img_A, label_A = t[0]
    img_B, label_B = t[1]

    new_label = int(label_A == label_B)

    X_pairs.append([img_A, img_B])
    y_pairs.append(new_label)
  
  X_pairs = np.array(X_pairs)
  y_pairs = np.array(y_pairs)

  return X_pairs, y_pairs

from keras.models import load_model
#from tensoflow.keras.models import load_model
import tensorflow as tf
from keras.callbacks import EarlyStopping 
#from tensorflow.keras.callbacks import EarlyStopping


def train_model(dataset : list, label:list):
    '''
    returns trained model for given dataset
    donot forget to save the model
    '''

    dataset = np.array(dataset)
    label  =np.array(label)

    model = load_model('A:/pj/canwesave.h5') # untrained model path must be given here

    model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              metrics=['accuracy'])

    data_pairs, label_pairs = make_paired_dataset(dataset,label)

    model.fit(x=[ data_pairs[:, 1, :, :],data_pairs[:, 0, :, :]],
          y=label_pairs,
          validation_split = 0.2,
          epochs=1,
          batch_size=32,
          callbacks=[EarlyStopping(patience=2)],
         )

    return model

def make_test_dataset(file_path1:str, file_path2:str)->list:
    '''
    takes two image to calculate similarity
    '''

    dataset = []

    image = cv2.imread(file_path1,cv2.COLOR_BGR2GRAY)
    image = Image.fromarray(image)
    image = image.resize((SIZE,SIZE))
    dataset.append(np.array(image))

    image = cv2.imread(file_path2,cv2.COLOR_BGR2GRAY)
    image = Image.fromarray(image)
    image = image.resize((SIZE,SIZE))
    dataset.append(np.array(image))

    return dataset


def predict(model,image_A:str, image_B:str)->int:#returns similarity in %
    
    data  = make_test_dataset(image_A, image_B)
    data = np.array(data)

    prediction = model.predict([data[0].reshape((1, SIZE,SIZE)), 
               data[1].reshape((1, SIZE,SIZE))])

    return prediction[0]*100



    
