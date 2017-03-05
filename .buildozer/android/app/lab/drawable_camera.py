import kivy

kivy.require('1.4.0')

from kivy.uix.camera import Camera
from kivy.graphics import *
import cv2

class DrawableCamera(Camera):
    selection = None
    drag_start = None
    tracking_state = 0
    draw_rect = None
    selection_corner = None
    selection_width = 200
    selection_image = None
    detector = None

    def on_tex(self, *l):
        super(DrawableCamera, self).on_tex(l)
        # process image and set new texture back to canvas
        view = self.detector.find_query_image(self._camera._raw_buffer)
        texture = self._camera.texture
        texture.blit_buffer(view.tostring(), colorfmt="bgr")


    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.selection_corner = touch.pos
            # mark selection from point
            if self.draw_rect:
                self.canvas.remove(self.draw_rect)
            self.draw_rect = InstructionGroup()
            self.draw_rect.add(Color(1, 0, 0, 0.2))
            w = self.selection_width/2
            line = Line(rectangle=[touch.pos[0]-w, touch.pos[1]-w, w*2, w*2], width=2)
            self.draw_rect.add(line)
            # self.draw_rect.add(Rectangle(pos=self.selection_corner, size=self.selection_size))
            self.canvas.add(self.draw_rect)
            subtexture = self.texture.get_region(touch.pos[0]-w, touch.pos[1]-w, w*2, w*2)

            b = self._camera._raw_buffer
            x0,x1 = int(touch.pos[0]-(w)), int(touch.pos[0]+(w))
            # opencv y axis starts at the top of the image and kivy at the bottom
            image_h = self._camera._resolution[1]
            y = image_h - touch.pos[1]
            y0,y1 = int(y), int(y+(w*2))
            # self.selection_image = b[y_i:y_f, x_i:x_f]

            self.detector.set_query_image(self._camera._raw_buffer, (x0, y0), (x1, y1))


            return True

        super(DrawableCamera, self).on_touch_down(touch)


    def set_detector(self, detector):
        self.detector = detector