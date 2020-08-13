# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 11:56:06 2020

This script produces an image containing circles that are
closely packed, but do not overlap. 

@author: Brian
"""

#%% Setup Environment

# Reset (clears all variables n stuff)
from IPython import get_ipython
get_ipython().magic('reset -sf')

import numpy as np

import math as m

from random import seed, randint

from skimage import draw, measure

from skimage.io import imshow

#%% INPUTS...

'''Image Options'''
s = 500 # width and height of frame

'''Stop Condition'''
passLimit = 500 # the stop condition

'''Size/Arrangement Options'''
rad_biggest  = s/10
rad_smallest = s/100
seed(1) # change the seed (i.e. 2,3,4,5...) if you want a different random arrangement

#%% Solve and Make the Mask 

# Make blank mask
mask = np.zeros([s,s], dtype=bool)

# Draw the first circle...
nCircles = 1
r,c = randint(0,s), randint(0,s)
rr,cc = draw.circle(r,c, rad_biggest, shape=(s,s)) # draw a circle with largest radius possible.
mask[rr, cc] = 1
nCircles = 1

testMask = np.zeros([500,500],dtype=bool)

nPasses=0
nAccepts=0

# Draw the other circles...
while(nPasses < passLimit):
       
    testMask = mask.copy()
    
    # Only pick a new centerpoint from available locations (where pixels=0)
    avail = np.where(mask == 0)
    nAvail = np.size(avail[0])
    randy = randint(0, nAvail)
    r,c = avail[0][randy], avail[1][randy]
    
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
        
        while(nRegions == nCircles and radius < rad_biggest):
                     
            mask = mask | testMask # take the previous one (which didn't have overlap)
            # images.append(mask)
            testMask = mask.copy() # new one becomes the old one
            radius = radius * 1.15 # Increase in 15% intervals.
            rr,cc = draw.circle(r,c, radius, shape=(s,s)) # draw a circle with largest radius possible.
            testMask[rr, cc] = 1
            label_image = measure.label(testMask) # calculate number of image regions.
            nRegions = np.max(label_image) # the maximum value in the label image.
    
    print('progress (sort of) = ', m.floor(nPasses/passLimit*100), '%')
    
imshow(mask)

print('DONE.')