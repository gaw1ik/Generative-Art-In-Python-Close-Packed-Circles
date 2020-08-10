# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 1:25:04 2020

@author: Brian
"""
#%% Setup Environment

from IPython import get_ipython
get_ipython().magic('reset -sf')

import numpy as np

# import cairo

import PIL

from random import seed, choice, randint

from matplotlib.pyplot import imshow, show

from skimage import draw, measure

import time

#%% INPUTS...

# GIF Options
filename = 'test4.gif'
s = 500 # width and height of frame
frame_duration = 1000/24
q1 = 5 # number of frames to hold before placing the first circle
q2 = 50 # number of frames to hold after the final circle is placed

# Stop Condition
passLimit = 50 # the stop condition

# Color Options
# R,G,B = 255,150,200 # test1
# R,G,B = 150,200,255 # test2
R,G,B = 150,255,200 # test3

# Size/Arrangement Options
rad_initial  = s/50
rad_smallest = s/100
seed(2)

#%% MAKE CANVAS AND 

print('Solving and Making Frames...')

# Make blank mask
mask = np.zeros([s,s], dtype=bool)

# Draw the first circle...
nCircles = 1
r,c = randint(0,s), randint(0,s)
rr,cc = draw.circle(r,c, rad_initial, shape=(s,s)) # draw a circle with largest radius possible.
mask[rr, cc] = 1
nCircles = 1

mask0 = mask

testMask = np.zeros([500,500],dtype=bool)

nPasses=0
nAccepts=0

images = []

# Draw the other circles...
while(nPasses < passLimit):
       
    testMask = mask.copy()
    
    # Only pick a new centerpoint from available locations (where pixels=0)
    avail = np.where(mask == 0)
    r,c = choice(avail[0]),choice(avail[1])
    
    radius = rad_smallest
    rr,cc = draw.circle(r,c, radius, shape=(s,s)) # draw a circle with largest radius possible.
    testMask[rr, cc] = 1
    
    label_image = measure.label(testMask) # calculate number of image regions.
    nRegions = np.max(label_image) # the maximum value in the label image.
        
    if nRegions < nCircles+1: # if the first guess didn't work out
        nPasses += 1
    else: # if the guess did work out
        # nDilateAttempts = 0 
        nAccepts += 1
        nCircles+=1
        
        while(nRegions == nCircles):
                     
            mask = mask | testMask # take the previous one (which didn't have overlap)
            images.append(mask)
            testMask = mask.copy() # new one becomes the old one
            radius = radius * 1.15 # Increase in 5% intervals.
            rr,cc = draw.circle(r,c, radius, shape=(s,s)) # draw a circle with largest radius possible.
            testMask[rr, cc] = 1
            label_image = measure.label(testMask) # calculate number of image regions.
            nRegions = np.max(label_image) # the maximum value in the label image.
    
imshow(mask)
# show()
# time.sleep(0.1)  
    
#%% Convert from Skimage to PIL images, and set up frames for GIF

print('Making PIL Image List...')

pilImages = []

# append q blank frames
blank = PIL.Image.new('RGB', (s,s))
for _ in range(q1):
    pilImages.append(blank)
    
# append q frames containing just the first circle
arr = np.zeros([s,s,3],dtype=np.uint8)
arr[:,:,0],arr[:,:,1],arr[:,:,2] = mask0*R,mask0*G,mask0*B
for _ in range(q1):
    im = PIL.Image.fromarray(arr,mode='RGB')
    pilImages.append(im)
    
# apend the rest of the frames (shows circles growing)
for image in images:
    arr[:,:,0] = image*R
    arr[:,:,1] = image*G
    arr[:,:,2] = image*B
    im = PIL.Image.fromarray(arr,mode='RGB')
    pilImages.append(im)
    
# freeze the final frame for a bit
for _ in range(q2):
    pilImages.append(im)

#%% Save as GIF
    
print('Saving GIF...')

pilImages[0].save(filename,
               save_all=True,
               append_images=pilImages[1:],
               optimize=False,
               duration=frame_duration,
               loop=0)

print('DONE.')