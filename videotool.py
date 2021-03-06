import cv2
import numpy as np

import cameramode

PROCESS_PERIOD = 5  # период обновления информации детекторами


class VideoTool:
    @staticmethod
    def draw_rectangle(frame, rectangle, color, thickness, label=None):
        cv2.rectangle(frame, (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]), color, thickness)
        if label is not None:
            y = rectangle[1] - 15 if rectangle[1] - 15 > 15 else rectangle[1] + 15
            cv2.putText(frame, label, (rectangle[0], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def __init__(self, src, init_fc = 0):
        self.set_video_source(src)
        self.color_people = (104, 176, 77)
        self.color_objects = (0, 255, 100)
        self.color_motion = (225, 252, 49)
        self.color_borders = (227, 28, 33)
        self.thickness_rectangle = 3
        self.thickness_border = 3
        self.frame_counter = init_fc
        self.last_gf_func = lambda frame: frame  # последний результат обработки (в виде функции)
        self.mode = cameramode.ORIGINAL
        self.object_detector = None
        self.motion_detector = None
        self.border_detector = None
        self.is_playing = True
        self.is_borders_mode = False
        print('VideoTool created:', self.fps, 'FPS')

    def set_video_source(self, src):
        self.video = cv2.VideoCapture(src)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.freq_ms = int(1000 / self.fps)
        self.frame_w = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_h = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # self.out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    def get_frame(self, original, width, height, mode=None, bgr_to_rgb=True):
        if original is None:
            retval, original = self.video.read()
        # TODO: обработать отсутствие кадра
        assert original is not None, 'Кадр не получен'
        if mode is None:
            mode = self.mode

        frame = cv2.resize(original, (width, height), interpolation=cv2.INTER_AREA)
        # bad code
        """if self.border_detector.is_drawing:
            cv2.imshow(self.border_detector.window_id, self.border_detector.draw_regions(frame))"""
        if bgr_to_rgb:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame_counter = (self.frame_counter + 1) % PROCESS_PERIOD
        if mode == cameramode.ORIGINAL:
            return frame

        if self.frame_counter == 0:
            if mode == cameramode.DETECT_OBJECTS:
                boxes, scores, labels = self.object_detector.process(frame)
                self.last_gf_func = lambda frame:  \
                    self.draw_detections(frame, boxes, labels)
            elif mode == cameramode.DETECT_MOTION:
                boxes = self.motion_detector.process(frame)
                self.last_gf_func = lambda frame: \
                    self.draw_detections(frame, boxes)
            else:
                self.last_gf_func = lambda frame: frame
        return self.last_gf_func(frame)

    def draw_detections(self, frame, boxes, labels=None):
        count = len(boxes)
        if labels is None:
            labels = [None] * count

        colors = []
        if self.mode == cameramode.DETECT_OBJECTS:
            for i in range(count):
                if labels[i] == self.object_detector.labels[1 - 1]:  # если человек
                    colors.append(self.color_people)
                else:
                    colors.append(self.color_objects)
        elif self.mode == cameramode.DETECT_MOTION:
            colors = [self.color_motion] * count
        else:
            return frame

        if self.is_borders_mode:
            frame = self.border_detector.draw_regions(frame, self.color_borders, self.thickness_border)
            are_rects_in_regs = self.border_detector.are_rectangles_in_regions(list(boxes))
            for i in range(count):
                if are_rects_in_regs[i]:
                    colors[i] = self.color_borders

        for i in range(count):
            self.draw_rectangle(frame, boxes[i], colors[i], self.thickness_rectangle, labels[i])
        return frame

    def get_security_detected(self, width=500, img=None):
        pass  # TODO

    def is_displayable(self):
        return self.mode == cameramode.ORIGINAL or \
               self.mode == cameramode.DETECT_OBJECTS or \
               self.mode == cameramode.DETECT_MOTION

    # def video_rec(self):
    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         if ret:
    #             out.write(frame)

    def play(self):
        self.is_playing = True

    def stop(self):
        self.is_playing = False

    def close(self):
        self.video.release()

    def set_mode(self, mode):
        self.mode = mode
        print('Mode is', self.mode)
