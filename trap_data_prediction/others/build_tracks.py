#!/usr/bin/env python
# coding: utf-8

# In[15]:


""""
Author        : Aditya Jain
Date started  : May 11, 2022
About         : given image sequences and annotation info, builds the tracks
"""

import cv2
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

from cost_method.iou import intersection_over_union


# #### User-Defined Inputs

# In[16]:


data_dir  = '/home/mila/a/aditya.jain/scratch/TrapData_QuebecVermont_2022/Quebec/'

# cost thresholding for removing false tracks
COST_THR  = 1   


# #### Variable Definitions

# In[17]:


image_dir   = data_dir + '2022_05_14/'
annot_file  = data_dir + 'localiz_annotation-2022_05_14.json'
track_file  = data_dir + 'tracking_annotation-2022_05_14.csv'

data_images = os.listdir(image_dir)
data_annot  = json.load(open(annot_file))

track_info  = []    # [<image_name>, <track_id>, <bb_topleft_x>, <bb_topleft_y>, <bb_botright_x>, <bb_botright_y>]
track_id    = 1


# #### Tracking Part

# In[18]:


def find_track_id(image_name, annot):
    """finds the track id for a given image and annotation"""
    
    global track_info    
    idx = -1
    
    while True:
        if track_info[idx][0] == image_name:
            if track_info[idx][2:6] == annot:
                return track_info[idx][1]            
        idx -= 1
    
    
def save_track(data_images, data_annot, idx):
    """
    finds the track between annotations of two consecutive images
    
    Args:
    data_images (list) : list of trap images
    data_annot (dict)  : dictionary containing annotation information for each image
    idx (int)          : image index for which the track needs to be found
    """
    
    global track_info, track_id, COST_THR
    
    image1_annot = data_annot[data_images[idx-1]][0]
    image2_annot = data_annot[data_images[idx]][0]
    cost_matrix  = np.zeros((len(image2_annot), len(image1_annot)))
    
    for i in range(len(image2_annot)):
        for j in range(len(image1_annot)):            
            iou              = intersection_over_union(image1_annot[j], image2_annot[i])
            cost             = 1-iou
            cost_matrix[i,j] = cost
            
    row_ind, col_ind = linear_sum_assignment(cost_matrix) 
    
    row_ind = list(row_ind)
    col_ind = list(col_ind)
    
    for i in range(len(image2_annot)):
        # have a previous match
        if i in row_ind:          
            row_idx = row_ind.index(i)
            col_idx = col_ind[row_idx]
            
            # have a reasonable match from previous frame
            if cost_matrix[i, col_idx] < COST_THR:
                cur_id  = find_track_id(data_images[idx-1], image1_annot[col_idx])
                track_info.append([data_images[idx], cur_id, 
                               image2_annot[i][0], image2_annot[i][1],
                               image2_annot[i][2], image2_annot[i][3],
                               image2_annot[i][0] + int((image2_annot[i][2]-image2_annot[i][0])/2),
                               image2_annot[i][1] + int((image2_annot[i][3]-image2_annot[i][1])/2)])
            
            # the cost of matching is too high; false match; thresholding; start a new track
            else:
                track_info.append([data_images[idx], track_id, 
                               image2_annot[i][0], image2_annot[i][1],
                               image2_annot[i][2], image2_annot[i][3],
                               image2_annot[i][0] + int((image2_annot[i][2]-image2_annot[i][0])/2),
                               image2_annot[i][1] + int((image2_annot[i][3]-image2_annot[i][1])/2)])
                track_id += 1
                
        # no match, this is a new track 
        else:
            track_info.append([data_images[idx], track_id, 
                               image2_annot[i][0], image2_annot[i][1],
                               image2_annot[i][2], image2_annot[i][3],
                               image2_annot[i][0] + int((image2_annot[i][2]-image2_annot[i][0])/2),
                               image2_annot[i][1] + int((image2_annot[i][3]-image2_annot[i][1])/2)])
            track_id += 1
    
    
def draw_bounding_boxes(image, annotation):
    """draws bounding box annotation for a given image"""

    for annot in annotation:
        cv2.rectangle(image,(annot[0], annot[1]),(annot[2], annot[3]),(0,0,255),3)
        
    return image
        


# #### Build the tracking annotation for the first image

# In[19]:


first_annot = data_annot[data_images[0]][0]

for i in range(len(first_annot)):
    track_info.append([data_images[0], track_id, 
                       first_annot[i][0], first_annot[i][1], 
                       first_annot[i][2], first_annot[i][3],
                       first_annot[i][0] + int((first_annot[i][2]-first_annot[i][0])/2),
                       first_annot[i][1] + int((first_annot[i][3]-first_annot[i][1])/2)])
    track_id += 1


# #### Build the tracking annotation for the rest images 

# In[20]:


# wrap this into a function

for i in range(1, len(data_images)):
    save_track(data_images, data_annot, i)

track_df = pd.DataFrame(track_info, columns =['image', 'track_id', 'bb_topleft_x', 
                                       'bb_topleft_y', 'bb_botright_x', 'bb_botright_y',
                                       'bb_centre_x', 'bb_centre_y'])

track_df.to_csv(track_file, index=False)





