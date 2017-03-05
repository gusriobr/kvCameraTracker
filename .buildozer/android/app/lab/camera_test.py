import kivy

kivy.require('1.4.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.core.window import Window

from drawable_camera import DrawableCamera
from tracking.feature_based.camera_tracker import TrackerDetector

import cv2

class MyApp(App):


    # Function to take a screenshot
    def doscreenshot(self, *largs):
        Window.screenshot(name='screenshot%(counter)04d.jpg')

    def _get_camera_resolution(self):
        cap = cv2.VideoCapture(0)
        return (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def build(self):
        #self.detector = FeatureDetector("brisk")
        self.detector = TrackerDetector("KCF")

        w,h = self._get_camera_resolution()
        camwidget = Widget()  # Create a camera Widget
        # cam = Camera()  # Get the camera
        cam = DrawableCamera(resolution=(w*1.5, h*1.5), size=(w*1.5, h*1.5))
        cam.set_detector(self.detector)
        cam.play = True  # Start the camera
        camwidget.add_widget(cam)

        button = Button(text='screenshot', size_hint=(0.12, 0.12))
        button.bind(on_press=self.doscreenshot)
        camwidget.add_widget(button)  # Add button to Camera Widget

        return camwidget


if __name__ == '__main__':
    MyApp().run()
