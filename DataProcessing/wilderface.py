# -*- coding: utf-8 -*-
"""superresolution.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1spHKj9mnf4pf9kyNMKoHM5fMVH88MS7v
"""

from PIL import Image
#import matplotlib.pyplot as plt
import numpy as np
import torchvision.datasets as datasets
from torchvision.transforms import ToTensor
import os

"""Download train and validation dataset. We pre-processed train and validation dataset with super-resolution."""

train_data = datasets.WIDERFace(
    root = 'data',
    split = 'train',                         
    transform = ToTensor(), 
    download = True        
)
val_data = datasets.WIDERFace(
    root = 'data', 
    split = 'val', 
    transform = ToTensor(),
    download = True
)

print(train_data)
print(val_data)

train_data.img_info[0]

train_data.img_info[0]['img_path']

train_data.img_info[0]

arr = train_data.img_info[3]['annotations']['blur'].numpy()
print(2 in arr)

"""Find blur == 2(heavy blur)"""

#return the indices of data_info with blur level == blur_level
def findBlur(data_info,blur_level):
  with open('./blur.txt','w') as f:
    blur_list = []
    for i in range(len(data_info)):
      #print(data_info[i]['annotations']['blur'])
      if blur_level in data_info[i]['annotations']['blur'].numpy():
        blur_list.append(i)
        f.write(str(i)+os.linesep)
    return blur_list

print(len(train_data.img_info))
train_heavy_blur = findBlur(train_data.img_info,2)
print("train_heavy_blur size: " + str(len(train_heavy_blur)))
print("heavy/total: " + str(len(train_heavy_blur)/len(train_data.img_info)))

print(len(val_data.img_info))
val_heavy_blur = findBlur(val_data.img_info,2)
print("val_heavy_blur size: " + str(len(val_heavy_blur)))
print("heavy/total: " + str(len(val_heavy_blur)/len(val_data.img_info)))

"""In the train data, there exist 4496 images contains heavy blur face, about 35% of the total train dataset. In the validation data, there exist 1164 images contains heavy blur face, about 36% of the total validation dataset. """

#def imgName(path):
#  return path[path.rindex('/')+1:]
#print(imgName(train_data.img_info[0]['img_path']))
print(train_data.img_info[0]['img_path'])
import shutil
import os


#put all the heavy blur image in one file
def collectBlurFiles(data_info,blur_list,path):
  print(len(blur_list))
  # Check whether the specified path exists or not
  if not os.path.exists(path):
    # Create a new directory because it does not exist
    os.makedirs(path)
  
  count = 0
  #with open('./blur_copied.txt','w') as f:
  for index in blur_list:
    src = data_info[index]['img_path']
    # name = imgName(src)
    # dst = path+'/'+name
    shutil.copy(src, path)
    count = count + 1
      #f.write(str(count) + ':' + src + os.linesep)

collectBlurFiles(train_data.img_info,train_heavy_blur,'./train_heavy_blur')
collectBlurFiles(val_data.img_info,val_heavy_blur,'./val_heavy_blur')
