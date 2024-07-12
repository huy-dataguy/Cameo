import cv2 as cv
import numpy as np
import time

class CaptureManager(object):
    def __init__(self, capture, previewWindowManager = None, 
                 shouldMirrorPreview = False):
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview
        self._capture = capture
        self._channel = 0
        self._enteredFrame = 0
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        
        self._videoWriter = None
        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

        # The single-underscore '_' prefix is just a convention, indicating
        #       that the variable should be treated as protected 
        #       (accessed only within the class and its subclasses).


        #The double-underscore '__' EX: MyClass.__myVariable
        #such a variable should be treated as private
        #        (accessed only within the class, and not its subclasses).


    @property 
    def channel(self):
        return self._channel
    
    #With @property, now we can access obj.channel instead of obj._channel
    @channel.setter
    def channel(self, value):
        if self.channel != value:
            self._channel = value
            self._frame = None
    

    @property
    def frame(self):
        _, self._frame = self._capture.retrieve(self._frame, self.channel)
        return self._frame
        #the underscore _ is often used as a "dummy" variable to discard unnecessary or unimportant values
        #example: tuple_value = (1,2, 3)
        #_, second, _ = tuple_value
        #print(second) # answer: 2

    @property
    def isWritingImage(self):
        return self._imageFilename is not None
    @property
    def isWritingVideo(self):
        return self._videoFilename is not None
    