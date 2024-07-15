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
    

    def enterFrame (self):
        # """      """: is located immediately after a definition a function or a class a module
        #          Purpose: used to provide a documentary or description about that function, class or mudole
        """Capture the next frame, if any"""



        #first check that any preveous frame was exited

        #The assert keyword is used when debugging code.
        #The assert keyword **lets you test if** a condition in **your code returns True**, 
        #       if not, the program will raise an AssertionError.
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        """Draw to the window. Estimate fps. Write file. Release frame"""
        if(self._frame == None):
            self._enteredFrame = False
            return
        
        #Update fps estimate
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        
        #increase frame to keep track the number frames that have been processed
        self._frameElapsed += 1


        #Draw window
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                #flip the frame left to right "fliplr"
                mirroredFrame = np.fliplr(self._frame)
                self.shouldMirrorPreview.show(mirroredFrame)
            else:
                self.shouldMirrorPreview.show(self._frame)
        
        # Write to the image file, if any.
        if self.isWritingImage:
            cv.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None
       
        # Write to the video file, if any.
        self._writeVideoFrame()
        # Release the frame.
        self._frame = None
        self._enteredFrame = False
    def writeImage(self, fileName):
        """Write the next exited frame to an image file"""
        self._imageFilename = fileName
    def startWritingVideo(self, fileName, encoding = cv.VideoWriter_fourcc('M','J','P','G')):
        self._videoFilename = fileName
        self._videoEncoding = encoding
    def stopWritingVideo(self):
        """stop writing exited frame to a video file"""
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None