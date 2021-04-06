import cv2
import depthai as dai
from PyQt5.QtCore import QThread, pyqtSignal


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()



class CaletaAPI:


    pipeline = None


    def __init__(self):
        self.pipeline =  dai.Pipeline()
        #self.initCamera()

    def initCamera(self,frame):
        # Define a source - color camera
        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(300, 300)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)


        # Create output
        xout_rgb = self.pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")

        #cam_rgb.preview.link(xout_rgb.input)


    def switchOnCamera(self, frame):
        with dai.Device(self.pipeline) as device:
            # Start pipeline
            device.startPipeline()

            # Output queue will be used to get the rgb frames from the output defined above
            q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

            while True:
                in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                #cv2.imshow("bgr",in_rg)
                # Retrieve 'bgr' (opencv format) frame
                cv2.imshow("bgr", in_rgb.getCvFrame())
                self.thread = VideoThread()
                # connect its signal to the update_image slot
                self.thread.change_pixmap_signal.connect(self.update_image)
                # start the thread
                self.thread.start()

                if cv2.waitKey(1) == ord('q'):
                   break