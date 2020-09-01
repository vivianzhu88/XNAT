from skimage.io import imsave, imread
import pydicom
import numpy as np
import re
import os
import pandas as pd

MAIN_FOLDER        = "/Users/vivianzhu/Documents/XNAT/temp/"

SUB_FOLDERS_PNG    = 'png/'
#FILE_LIST        = ['./data/files_A.txt']
FILE_LIST         = ['ID_0a0a9691a.dcm', 'ID_0a0a9133e.dcm', 'ID_0a0a9a8ef.dcm']

CSV_NAMES        = 't.csv'


WINDOW_CENTER    = 50
WINDOW_WIDTH    = 100

RGB                = True

def get_first_of_dicom_field_as_int(x):
    #get x[0] as in int is x is a 'pydicom.multival.MultiValue', otherwise get int(x)
    if type(x) == pydicom.multival.MultiValue:
        return int(x[0])
    else:
        return int(x)

'''
def get_files_list(file_list):
    train_files = []
    with open(file_list, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.rstrip()
            train_files.append(line)
    
    return train_files
'''
  
def get_gray_img(dicom, window_center, window_width):
    try:
        img = dicom.pixel_array
        slope = get_first_of_dicom_field_as_int(dicom.RescaleSlope)
        intercept = get_first_of_dicom_field_as_int(dicom.RescaleIntercept)
        #window_center = get_first_of_dicom_field_as_int(dicom.WindowCenter)
        #window_width = get_first_of_dicom_field_as_int(dicom.WindowWidth)
        #window_center = WINDOW_CENTER
        #window_width = WINDOW_WIDTH

        img = (img*slope +intercept)
        img_min = window_center - window_width//2
        img_max = window_center + window_width//2
        img[img<img_min] = img_min
        img[img>img_max] = img_max

        img = (img - img_min) / (img_max - img_min)
        return img
    except:
        return None

def process_dicom(dicom, rgb=True):
    brain_img = get_gray_img(dicom, 40, 80)
    subdural_img = get_gray_img(dicom, 80, 200)
    bone_img = get_gray_img(dicom, 600, 2000)

    if not brain_img is None and not subdural_img is None and not bone_img is None:
        bsb_img = np.zeros((brain_img.shape[0], brain_img.shape[1], 3))
        bsb_img[:, :, 0] = brain_img
        bsb_img[:, :, 1] = subdural_img
        bsb_img[:, :, 2] = bone_img
        return bsb_img
    return None
    




    
train_files = [MAIN_FOLDER + x for x in FILE_LIST]

ids = []
for file in train_files:
    print(file)
    ds = pydicom.dcmread(file)
    img = process_dicom(ds, rgb=RGB)
    if not img is None:
        splits = re.split('_|\.', file)
        img_id = splits[len(splits) - 2]
        print(img_id)
        ids.append(img_id)
        imsave(MAIN_FOLDER + SUB_FOLDERS_PNG + str(img_id) + '.png', img)

df = pd.DataFrame()
df['ID'] = ids
df.to_csv(MAIN_FOLDER + CSV_NAMES, index=False)
