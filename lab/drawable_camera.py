import kivy

kivy.require('1.4.0')

from kivy.uix.camera import Camera
from kivy.graphics import *


class DrawableCamera(Camera):
    selection = None
    drag_start = None
    tracking_state = 0
    draw_rect = None
    selection_corner = None
    selection_width = 200
    selection_image = None

    def on_tex(self, *l):
        super(DrawableCamera, self).on_tex(l)

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

            return True
        super(DrawableCamera, self).on_touch_down(touch)

    #	Method	to	track	mouse	events
    def mouse_event(self, event, x, y, flags, param):
        x, y = np.int16([x, y])
        #	Detecting	the	mouse	button	down	event
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            self.tracking_state = 0
            # return
        if self.drag_start:
            # if event == cv2.EVENT_LBUTTONUP:
            # if event == cv2.EVENT_RBUTTONDOWN:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                h, w = self.frame.shape[:2]
                xo, yo = self.drag_start
                x0, y0 = np.maximum(0, np.minimum([xo, yo], [x, y]))
                x1, y1 = np.minimum([w, h], np.maximum([xo, yo], [x, y]))
                self.selection = None
                if x1 - x0 > 0 and y1 - y0 > 0:
                    self.selection = (x0, y0, x1, y1)
            else:
                # self.drag_start = None
                if self.selection is not None:
                    self.tracking_state = 1
                    if self.detector:
                        # extract selected imagen
                        x0, y0, x1, y1 = self.selection
                        #img = self.extract_foreground(self.frame, self.selection)
                        self.detector.set_query_image(self.frame, (x0, y0),(x1, y1))


    def start_tracking(self):
        #	Iterate	until	the	user	presses	the	Esc	key
        while True:
        # Capture	the	frame	from	webcam
            ret, self.frame = self.cap.read()
            #	Resize	the	input	frame
            self.frame = cv2.resize(self.frame, None,
                                    fx=self.scaling_factor,
                                    fy=self.scaling_factor,
                                    interpolation=cv2.INTER_AREA)

            view = self.frame

            if self.selection:
                x0, y0, x1, y1 = self.selection
                self.track_window = (x0, y0, x1 - x0, y1 - y0)
                # on selection end
                BORDER = 2
                cv2.rectangle(self.frame, (x0-BORDER, y0-BORDER), (x1+BORDER, y1+BORDER), (0, 255, 0), 2)

            if self.tracking_state == 1:
                self.selection = None
                view = self.detector.find_query_image(view)

            cv2.imshow('Object	Tracker', view)
            c = cv2.waitKey(5)
            if c == 27:
                break