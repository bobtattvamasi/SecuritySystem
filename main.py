import logging
import sys
import time
import traceback
import gc

import cv2
import tensorflow as tf
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime

from threading import Thread, Lock, Event

#import design
import mainwindow
import settings
import log

import cameramode
from videotool import VideoTool
from videoview import VideoView
from frame_analysis.object_detector import ObjectDetector
from frame_analysis.border_detector import BorderDetector
from frame_analysis.motion_detector import MotionDetector

from datetime import datetime

duration = 1000  # millisecond
freq = 440  # Hz

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

CAMERAS_COUNT = 3
CONFIDENCE_LEVEL = 0.7  # HERE - нижний порог уверенности модели от 0 до 1.
                        # 0.7 - объект в кадре будет обведён рамкой, если
                        #       сеть уверена на 70% и выше
CLASSES_TO_DETECT = [
    1,      # person
    17,     # cat
    18      # dog
]  # HERE - классы для обнаружения, см. файл classes_en.txt
   # номер класса = номер строки, нумерация с 1


def get_image_qt(frame):
    # решает проблему с искажением кадров
    height, width, channels = np.shape(frame)
    totalBytes = frame.nbytes
    bytesPerLine = int(totalBytes / height)

    qimg = QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)

# Иконка загрузки
class Splash(QSplashScreen):
    def __init__(self, *arg, **args):
        QSplashScreen.__init__(self, *arg, **args)
        self.setCursor(Qt.BusyCursor)
        self.setPixmap(QPixmap("resources/boot.jpg"))
        loaut = QVBoxLayout(self)
        loaut.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding))
        #self.progress = QProgressBar(self)
        #self.progress.setValue(0)
        #self.progress.setMaximum(100)
        #loaut.addWidget(self.progress)
        #self.showMessage(u"Пример заставки", Qt.AlignTop)
        #self.startTimer(1000)
        #self.progress.setMaximum(0)
    #def timerEvent(self, event):
        #self.progress.setValue(self.progress.value() + 1)
        #event.accept()



# Окно Настроек
class SettingsWindow(QWidget, settings.Ui_SettingsForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Settings')
        self.returnButton.clicked.connect(self.returnToMain)
        self.setWindowIcon(QIcon("icon_settings.png"))

    def returnToMain(self, event):
        self.close()
        self.destroy()


# Окно Log'a
class LogWindow(QWidget, log.Ui_Log):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Log')
        self.pushButton.clicked.connect(self.returnToMain)
        self.setWindowIcon(QIcon("icon_log.png"))

    def returnToMain(self, event):
        self.close()
        self.destroy()


class SecondWindow(QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, Qt.Window)
        self.setWindowTitle('Settings')
        self.build()

    def build(self):
        self.mainLayout = QVBoxLayout()

        self.buttons = []
        for i in range(5):
            but = QPushButton('button {}'.format(i), self)
            self.mainLayout.addWidget(but)
            self.buttons.append(but)
        self.setLayout(self.mainLayout)


class VideoWorker(Thread):
    def __init__(self, name, videotool, videoview, mutex, stop_event):
        super().__init__(name=name)
        self.vtool = videotool
        self.vview = videoview
        self.mutex = mutex
        self.stop_event = stop_event

        self.emergency_stop = False
        self.last_frame = None
        self.reader = Thread(target=self.read_stream, args=[stop_event])

    def read_stream(self, stop_event):
        print('{}: let\'s read the stream!'.format(self.getName()))
        try:
            while not stop_event.is_set() and not self.emergency_stop:
                ret, self.last_frame = self.vtool.video.read()
        except:
            print('{} - unexpected error: {}'.format(self.getName(), traceback.format_exc()))
        print('{}: done!'.format(self.getName()))

    def run(self):
        self.reader.start()
        try:
            while not self.stop_event.is_set():
                # time_start = datetime.now()
                self.mutex.acquire()
                if not self.stop_event.is_set() and self.last_frame is not None:
                    self.tick()
                self.mutex.release()
                # elapsed_ms = (datetime.now() - time_start).microseconds / 1000
                # print(elapsed_ms, 'ms elapsed')
                # time.sleep(max(0, self.vtool.freq_ms - elapsed_ms) / 1000)
            print('It\'s {}, goodbye!'.format(self.getName()))
        except:
            print('{} - unexpected error: {}'.format(self.getName(), traceback.format_exc()))
            self.emergency_stop = True
            if self.mutex.locked():
                self.mutex.release()
        self.reader.join()

    # Действия, которые выполняются над каждым кадром
    def tick(self):
        if self.vtool.is_displayable() and self.vtool.is_playing:
            container = self.vview.video_label_container

            ratio_w = container.width() / self.vtool.frame_w
            ratio_h = container.height() / self.vtool.frame_h
            ratio = min(ratio_w, ratio_h)

            if self.vtool.border_detector.is_drawing:
                frame = self.vtool.get_frame(self.last_frame,
                                             int(self.vtool.frame_w * ratio),
                                             int(self.vtool.frame_h * ratio),
                                             mode=cameramode.ORIGINAL,
                                             bgr_to_rgb=False)
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow(self.vtool.border_detector.window_id,
                           self.vtool.border_detector.draw_regions(frame,
                           self.vtool.color_borders,
                           self.vtool.thickness_border))
                """if cv2.waitKey(self.vtool.freq_ms) == ord('q'):  # ??? HOWTO?
                    print('qq!')
                    self.vview.borders_btn.click()"""
            else:
                frame = self.vtool.get_frame(self.last_frame,
                                             int(self.vtool.frame_w * ratio),
                                             int(self.vtool.frame_h * ratio))
                frame = get_image_qt(frame)
                self.vview.video_label.setPixmap(frame)

    def start(self):
        print('Hello, I\'m {}'.format(self.getName()))
        self.emergency_stop = False
        super().start()


class SecurityDetectorWorker(Thread):
    def __init__(self, name, video_capture, object_detector,
                 checking_period_sec, checking_burst, mutex, stop_event):
        super().__init__(name=name)
        self.video_capture = video_capture
        self.object_detector = object_detector
        self.checking_period_sec = checking_period_sec
        self.checking_burst = checking_burst
        self.mutex = mutex
        self.stop_event = stop_event

        self.security_prev_state = False
        self.security_curr_state = False
    
    def run(self):
        try:
            self.tick()
            while not self.stop_event.is_set():
                waiting_start_time = datetime.now()
                while (datetime.now() - waiting_start_time).seconds < self.checking_period_sec:
                    self.video_capture.read()
                    if self.stop_event.is_set():
                        break;
                # time_start = datetime.now()
                self.mutex.acquire()
                if not self.stop_event.is_set():
                    self.tick()
                self.mutex.release()
                # elapsed_ms = (datetime.now() - time_start).microseconds / 1000
                # print(elapsed_ms, 'ms elapsed')
                # time.sleep(max(0, self.vtool.freq_ms - elapsed_ms) / 1000)
            print('It\'s {}, goodbye!'.format(self.getName()))
        except:
            print('{} - unexpected error: {}'.format(self.getName(), traceback.format_exc()))
            if self.mutex.locked():
                self.mutex.release()

    # Действия, которые выполняются над каждым кадром
    def tick(self):
        print('Let\'s check...')
        self.security_prev_state = self.security_curr_state
        self.security_curr_state = False
        log_str = ''
        for i in range(self.checking_burst):
            if self.stop_event.is_set():
                return

            frame = self.video_capture.read()[1]
            boxes, scores, classes = self.object_detector.process(frame)
            if len(boxes) > 0:
                self.security_curr_state = True
                break

        if self.security_curr_state != self.security_prev_state:
            log_str = '{} - охранник {}'.format(datetime.now().\
                    strftime('%d.%m.%y %H:%M'),\
                    'на месте' if self.security_curr_state else 'отсутствует')

        print('Log:', log_str)
        if(log_str != ''):
            with open('log.txt', 'a') as f:
                f.write(log_str + '\r\n')

    def start(self):
        print('Hello, I\'m {}'.format(self.getName()))
        super().start()



class UI(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.image = None
        self.width_standard = 1200
        self.width360 = 1600

        vsrcs = [None] * 4
        secsrc = None
        videosource = 'cameras'
        if len(sys.argv) > 1:
            videosource = sys.argv[1]

        if (videosource == 'files'):
            vsrcs[0] = '../cat.mp4'
            vsrcs[1] = '../cat.mp4'
            vsrcs[2] = '../people.mp4'
            vsrcs[3] = '../people.mp4'
            secsrc = '../people.mp4'
        else:
            vsrcs[0] = 'rtsp://192.168.1.203:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            vsrcs[1] = 'rtsp://192.168.1.135:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            vsrcs[2] = 'rtsp://192.168.1.163:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            vsrcs[3] = 0
            secsrc = 0

        vv_positions = [(1, 1, 1, 1),  # Позиции создаваемых VideoView в сетке
                        (1, 2, 1, 1),  # (строка, столбец, ширина, высота)
                        (2, 1, 2 if CAMERAS_COUNT == 3 else 1, 1),
                        (2, 2, 1, 1)
                       ]

        model_name = 'nn_model'  # faster_rcnn_inception_v2_coco_2018_01_28
        model_path = model_name + '/frozen_inference_graph.pb'
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        labels = []
        labels_path = 'classes_en.txt'  # HERE - файл с подписями для классов
        with open(labels_path) as f:
            labels = f.readlines()
        labels = [s.strip() for s in labels]

        # Инициализация инструментария для каждого видеопотока
        self.videotools = []
        self.videoviews = []
        self.mutexes = []
        self.stop_cam_threads_event = Event()
        for i in range(CAMERAS_COUNT):
            self.videotools.append(VideoTool(src=vsrcs[i], init_fc=i))
            self.videotools[i].object_detector = ObjectDetector(detection_graph=detection_graph,
                                                                labels=labels,
                                                                classes_to_detect=CLASSES_TO_DETECT,
                                                                confidence_level=CONFIDENCE_LEVEL)
            self.videotools[i].border_detector = BorderDetector()
            self.videotools[i].motion_detector = MotionDetector()

            self.videoviews.append(VideoView(self, caption='Камера №'+str(i+1)))
            row, col, w, h = vv_positions[i]
            self.main_grid.addWidget(self.videoviews[i], row, col, h, w)

            self.videoviews[i].mode_cb.currentIndexChanged.\
                connect(self.videotools[i].set_mode)

            def borders_slot(event, i=i):
                vtool = self.videotools[i]
                vview = self.videoviews[i]

                self.mutexes[i].acquire()
                if vtool.border_detector.is_drawing:
                    vtool.border_detector.end_selecting_region()
                    vtool.is_borders_mode = vtool.border_detector.has_regions
                    vview.borders_btn.setText('Очистить границы'\
                                              if vtool.is_borders_mode else\
                                              'Обозначить границы')
                else:
                    if vtool.is_borders_mode:
                        vtool.border_detector.clear_points()
                        vtool.is_borders_mode = False
                        vview.borders_btn.setText('Обозначить границы')
                    else:
                        vview.video_label.pixmap().fill(QColor(0, 0, 0))
                        vtool.border_detector.start_selecting_region(\
                            str(datetime.now()))
                        vview.borders_btn.setText('Сохранить границы')
                self.mutexes[i].release()

            self.videoviews[i].borders_btn.clicked.connect(borders_slot)
            self.mutexes.append(Lock())

        self.security_capture = cv2.VideoCapture(secsrc)
        self.security_detector = ObjectDetector(detection_graph=detection_graph,
                                                labels=labels,
                                                classes_to_detect=[1],  # person
                                                confidence_level=CONFIDENCE_LEVEL)
        self.security_mutex = Lock()
        self.stop_security_event = Event()

        self.setWindowTitle('Security System')
        self.log_btn.clicked.connect(self.log_open)
        self.refresh_btn.clicked.connect(self.refresh_cameras)
        self.refresh_btn.clicked.connect(self.refresh_security_cam)
        self.settings_btn.clicked.connect(self.settings_open)
        self.exit_btn.clicked.connect(self.close)
        self.settings_window = None
        self.log_window = None

    # Запускает обработку всех видеопотоков в отдельных потоках выполнения
    def start_cam_threads(self):
        self.cam_threads = []
        for i in range(CAMERAS_COUNT):
            self.cam_threads.append(VideoWorker('VideoWorker' + str(i),
                                                self.videotools[i],
                                                self.videoviews[i],
                                                self.mutexes[i],
                                                self.stop_cam_threads_event))
            self.cam_threads[i].start()

    def start_security_thread(self):
        self.security_thread = SecurityDetectorWorker(name='SecurityDetector',
                                                      video_capture=self.security_capture,
                                                      object_detector=self.security_detector,
                                                      checking_period_sec=10,
                                                      checking_burst=5,
                                                      mutex=self.security_mutex,
                                                      stop_event=self.stop_security_event)
        self.security_thread.start()

    # Сообщает всем отдельным потокам выполнения, что обработка больше не нужна
    def stop_cam_threads(self):
        self.stop_cam_threads_event.set()

    def stop_security_thread(self):
        self.stop_security_event.set()

    def stop_cam_threads_and_wait(self):
        self.stop_cam_threads()
        for i in range(CAMERAS_COUNT):
            self.cam_threads[i].join()
            print('Goodbye, {}!'.format(self.cam_threads[i].getName()))
        print('All camera threads are stopped')

    def stop_security_thread_and_wait(self):
        self.stop_security_thread()
        self.security_thread.join()
        print('Goodbye, {}!'.format(self.security_thread.getName()))

    def settings_open(self, event):
        #print("it's realy settingsButton")
        if not self.settings_window:
            self.settings_window = SettingsWindow()
        self.settings_window.show()

    def log_open(self, event):
        if not self.log_window:
            self.log_window = LogWindow()
        self.log_window.show()
        with open("log.txt", 'r') as f:
            mytext = f.read()
            self.log_window.textEdit.setPlainText(mytext)

    def refresh_cameras(self):
        self.stop_cam_threads_and_wait()
        self.stop_cam_threads_event.clear()
        self.start_cam_threads()

    def refresh_security_cam(self):
        self.stop_security_thread_and_wait()
        self.stop_security_event.clear()
        self.start_security_thread()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Вы действительно хотите закрыть охранную систему?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.stop_cam_threads_and_wait()
            self.stop_cam_threads_event.clear()
            for i in range(CAMERAS_COUNT):
                # self.mutexes[i].acquire()
                # self.cam_threads[i].stop_gracefully()
                self.videotools[i].close()
                # self.mutexes[i].release()

            self.stop_security_thread_and_wait()
            self.stop_cam_threads_event.clear()
            self.security_capture.release()
            if len(self.videotools) > 0:
                self.videotools[0].object_detector.close()
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    splash = Splash()
    splash.show()
    window = UI()  # Создаём объект класса ExampleApp
    window.videotools[0].object_detector.process(np.zeros((1, 1, 3)))
    #window.setWindowOpacity(0.5)
    # pal = window.palette()
    # pal.setBrush(QPalette.Normal, QPalette.Background,
    #              QBrush(QPixmap("resources/Fone.jpg")))
    # window.setPalette(pal)
    # window.setAutoFillBackground(True)
    window.start_cam_threads()
    window.start_security_thread()
    time.sleep(2)
    window.show()  # Показываем окно
    splash.finish(window)
    app.exec_()  # и запускаем прило


if __name__ == '__main__':
    main()