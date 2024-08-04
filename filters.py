import cv2 as cv
import numpy as np
import utils

def strokeEdges(src, dst, blurKsize = 7, edgeKsize = 5):
    # Apply median blur to reduce noise
    if blurKsize >= 3:
        blurredSrc = cv.medianBlur(src, blurKsize)
        graySrc = cv.cvtColor(blurredSrc, cv.COLOR_BGR2GRAY)
    else:
        graySrc = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    
    # Apply Laplacian operator to detect edges
    cv.Laplacian(graySrc, cv.CV_8U, graySrc, ksize = edgeKsize)
    
    # Normalize the inverse of the edge-detected image
    normalizedInverseAlpha = (1.0 / 255) * (255 - graySrc)
    
    # Split the source image into its color channels
    channels = cv.split(src)
    
    # Darken edges in each channel
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha
    
    # Merge the channels back into the destination image
    cv.merge(channels, dst)
