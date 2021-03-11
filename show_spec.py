import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from drug_design_UI import Ui_ReactionMonitor
# from PIL import Image
# import cv2
import random


class show_photo(QMainWindow, Ui_ReactionMonitor, QThread):
    def __init__(self, parent=None):
        super(show_photo, self).__init__(parent)
        self.setupUi(self)

        # 改下急停按钮颜色，急停退出
        self.e_stop.setStyleSheet("background-color: red")

        # 土味迭代器，21张图循环播放
        self.raman_list = ["Raman1", "Raman2", "Raman3", "Raman4", "Raman5", "Raman6", "Raman7",
                           "Raman8", "Raman9", "Raman10", "Raman11", "Raman12", "Raman13", "Raman14",
                           "Raman15", "Raman16", "Raman17", "Raman18", "Raman19", "Raman20", "Raman21"]
        self.ftir_list = ["FTIR1", "FTIR2", "FTIR3", "FTIR4", "FTIR5", "FTIR6", "FTIR7",
                          "FTIR8", "FTIR9", "FTIR10", "FTIR11", "FTIR12", "FTIR13", "FTIR14",
                          "FTIR15", "FTIR16", "FTIR17", "FTIR18", "FTIR19", "FTIR20", "FTIR21"]
        self.raman_iterator = 1
        self.ftir_iterator = 1
        self.switch_buffer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # 初始显示图片
        self.ftir_spec.setPixmap(QPixmap("./img/" + self.ftir_list[0]))
        self.ftir_spec.setScaledContents(True)
        self.raman_spec.setPixmap(QPixmap("./img/" + self.raman_list[0]))
        self.raman_spec.setScaledContents(True)

        # 按钮的连接
        self.ftir_get.clicked.connect(self.show_ir_clicked)
        self.raman_get.clicked.connect(self.show_raman_clicked)
        self.e_stop.clicked.connect(self.e_quit)
        self.switch1.clicked.connect(self.change_text1)
        self.switch2.clicked.connect(self.change_text2)
        self.switch3.clicked.connect(self.change_text3)
        self.switch4.clicked.connect(self.change_text4)
        self.switch5.clicked.connect(self.change_text5)
        self.switch6.clicked.connect(self.change_text6)
        self.switch7.clicked.connect(self.change_text7)
        self.switch8.clicked.connect(self.change_text8)
        self.switch9.clicked.connect(self.change_text9)
        self.switch10.clicked.connect(self.change_text10)

        # 图片自动刷新线程
        self.thread1 = backend_refresh()
        self.thread1.update_pic.connect(self.update_all)
        # 状态自动刷新线程
        self.thread2 = status_update()
        self.thread2.update_status.connect(self.refresh_status)
        # 线程启动
        self.thread1.start()
        self.thread2.start()

    def show_ir_clicked(self):
        self.ftir_spec.setPixmap(QPixmap("./img/" + self.ftir_list[self.ftir_iterator]))
        # self.ftir_spec.setScaledContents(True)
        self.ftir_iterator += 1
        if self.ftir_iterator == 21:
            self.ftir_iterator = 0

    def show_raman_clicked(self):
        self.raman_spec.setPixmap(QPixmap("./img/" + self.raman_list[self.raman_iterator]))
        # self.raman_spec.setScaledContents(True)
        self.raman_iterator += 1
        if self.raman_iterator == 21:
            self.raman_iterator = 0

    def update_all(self, signal):
        self.raman_spec.setPixmap(QPixmap("./img/" + self.raman_list[self.raman_iterator]))
        self.ftir_spec.setPixmap(QPixmap("./img/" + self.ftir_list[self.ftir_iterator]))
        self.ftir_iterator += 1
        self.raman_iterator += 1
        if self.raman_iterator == 21:
            self.raman_iterator = 0
        if self.ftir_iterator == 21:
            self.ftir_iterator = 0
        print("thread ok")

    # 更新采集到的状态
    def refresh_status(self, signal):
        temp = str(random.uniform(21, 23))[:4]
        flow = str(random.uniform(0.5, 0.7))[:4]
        pressure = str(random.uniform(0.150, 0.160))[:5]
        stir = str(random.randint(445, 455))
        PH = str(random.uniform(6.77, 6.99))[:4]

        self.temp_display.setText(temp + " C")
        self.flow_display.setText(flow + " ml/min")
        self.pressure_display.setText(pressure + " MPA")
        self.Stir_display.setText(stir + " RPM")
        self.ph_display.setText(PH)

    # 十个开关变色变字土味实现
    def change_text1(self):
        if self.switch_buffer[0] == 0:
            self.switch1.setText("ON")
            self.switch1.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[0] = 1
        else:
            self.switch1.setText("OFF")
            self.switch1.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[0] = 0

    def change_text2(self):
        if self.switch_buffer[1] == 0:
            self.switch2.setText("ON")
            self.switch2.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[1] = 1
        else:
            self.switch2.setText("OFF")
            self.switch2.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[1] = 0

    def change_text3(self):
        if self.switch_buffer[2] == 0:
            self.switch3.setText("ON")
            self.switch3.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[2] = 1
        else:
            self.switch3.setText("OFF")
            self.switch3.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[2] = 0

    def change_text4(self):
        if self.switch_buffer[3] == 0:
            self.switch4.setText("ON")
            self.switch4.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[3] = 1
        else:
            self.switch4.setText("OFF")
            self.switch4.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[3] = 0

    def change_text5(self):
        if self.switch_buffer[4] == 0:
            self.switch5.setText("ON")
            self.switch5.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[4] = 1
        else:
            self.switch5.setText("OFF")
            self.switch5.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[4] = 0

    def change_text6(self):
        if self.switch_buffer[5] == 0:
            self.switch6.setText("ON")
            self.switch6.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[5] = 1
        else:
            self.switch6.setText("OFF")
            self.switch6.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[5] = 0

    def change_text7(self):
        if self.switch_buffer[6] == 0:
            self.switch7.setText("ON")
            self.switch7.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[6] = 1
        else:
            self.switch7.setText("OFF")
            self.switch7.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[6] = 0

    def change_text8(self):
        if self.switch_buffer[7] == 0:
            self.switch8.setText("ON")
            self.switch8.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[7] = 1
        else:
            self.switch8.setText("OFF")
            self.switch8.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[7] = 0

    def change_text9(self):
        if self.switch_buffer[8] == 0:
            self.switch9.setText("ON")
            self.switch9.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[8] = 1
        else:
            self.switch9.setText("OFF")
            self.switch9.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[8] = 0

    def change_text10(self):
        if self.switch_buffer[9] == 0:
            self.switch10.setText("ON")
            self.switch10.setStyleSheet("background-color: lightGreen")
            self.switch_buffer[9] = 1
        else:
            self.switch10.setText("OFF")
            self.switch10.setStyleSheet("background-color: lightGrey")
            self.switch_buffer[9] = 0

    def e_quit(self):
        os._exit(0)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self, 'Reaction Monitor', "Are you sure to Exit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()

    def uchar_checksum(self, check_data, byteorder='little'):
        '''
        char_checksum 按字节计算校验和。每个字节被翻译为无符号整数
        @param check_data: 字节串
        @param byteorder: 大/小端
        '''
        length = len(check_data)
        checksum = 0
        for i in range(0, length):
            checksum += int.from_bytes(check_data[i:i + 1], byteorder, signed=False)
            checksum &= 0xFF  # 强制截断

        return checksum


class backend_refresh(QThread):

    update_pic = pyqtSignal(str)

    def __init__(self, parent=None):
        super(backend_refresh, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        while 1:
            self.update_pic.emit("0")  # 这个信号必须是string
            # 线程休眠5秒，五秒图片自动刷新，等不及的话可以按按钮刷新。
            self.sleep(5)


class status_update(QThread):

    update_status = pyqtSignal(str)

    def __init__(self, parent=None):
        super(status_update, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        while 1:
            self.update_status.emit("1")  # 这个信号必须是string
            # 线程休眠0.4秒，自动更新当前状态。
            self.msleep(400)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = show_photo()
    mainWindow.show()
    sys.exit(app.exec_())
