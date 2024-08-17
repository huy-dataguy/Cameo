import cv2 as cv
from managers import CaptureManager, WindowManager
import filters
import depth

class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('Cameo', self.onKeypress)
        
        self._captureManager = CaptureManager(cv.VideoCapture(0), self._windowManager, True)
        # self.filter = filters.SharpenFilter()
        self.filter = filters.FindEdgesFilter()
        # self.filter = filters.EmbossFilter()
        # self.filter = filters.BlurFilter()
        # self.filter = filters.Kernel5x5()

    def run(self):
        """Run main loop"""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            if frame is not None:
                # filters.strokeEdges(frame, frame)
                self.filter.apply(frame, frame)
              

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeypress(self, keycode):
        """handle a keypress
        space: take a screenshot
        tab: start/stop recording a screencast
        escape: quit
        """

        if keycode == 32: #space
            self._captureManager.writeImage('Screenshot.png')
        elif keycode == 9: #tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: #escape
            self._windowManager.destroyWindow()


if __name__ =="__main__":
    Cameo().run()