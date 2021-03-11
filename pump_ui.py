import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QCursor, QImage, QPixmap
import zerorpc


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


class ControlUnit(QtWidgets.QVBoxLayout):
    def __init__(self, MainWindow, index):
        super(ControlUnit, self).__init__()

        self.centralwidget = MainWindow.centralwidget
        self.controller = MainWindow.controller
        self.pump_config = MainWindow.pump_config
        self.index = index

        self.setObjectName("pump_control_%d" % self.index)
        self.pump_control_layer1 = QtWidgets.QHBoxLayout()
        self.pump_control_layer1.setObjectName("pump_control_layer1_%d" % self.index)
        self.label_command = QtWidgets.QLabel(self.centralwidget)
        self.label_command.setObjectName("label_command_%d" % self.index)
        self.pump_control_layer1.addWidget(self.label_command)
        self.command = QtWidgets.QLineEdit(self.centralwidget)
        self.command.setObjectName("command_%d" % self.index)
        self.pump_control_layer1.addWidget(self.command)
        self.label_parameter = QtWidgets.QLabel(self.centralwidget)
        self.label_parameter.setObjectName("label_parameter_%d" % self.index)
        self.pump_control_layer1.addWidget(self.label_parameter)
        self.parameter = QtWidgets.QLineEdit(self.centralwidget)
        self.parameter.setObjectName("parameter_%d" % self.index)
        self.pump_control_layer1.addWidget(self.parameter)
        self.addLayout(self.pump_control_layer1)

        self.pump_control_layer2 = QtWidgets.QHBoxLayout()
        self.pump_control_layer2.setObjectName("pump_control_layer2_%d" % self.index)
        self.label_address = QtWidgets.QLabel(self.centralwidget)
        self.label_address.setObjectName("label_address_%d" % self.index)
        self.pump_control_layer2.addWidget(self.label_address)
        self.address = QtWidgets.QComboBox(self.centralwidget)
        self.address.setObjectName("address_%d" % self.index)
        self.pump_control_layer2.addWidget(self.address)
        self.send_command_pb = QtWidgets.QPushButton(self.centralwidget)
        self.send_command_pb.setObjectName("send_command_pb_%d" % self.index)
        self.pump_control_layer2.addWidget(self.send_command_pb)
        self.addLayout(self.pump_control_layer2)

        self.pump_control_layer3 = QtWidgets.QHBoxLayout()
        self.pump_control_layer3.setObjectName("pump_control_layer3_%d" % self.index)
        self.reset_pb = QtWidgets.QPushButton(self.centralwidget)
        self.reset_pb.setObjectName("reset_pb_%d" % self.index)
        self.pump_control_layer3.addWidget(self.reset_pb)
        self.clear_position_pb = QtWidgets.QPushButton(self.centralwidget)
        self.clear_position_pb.setObjectName("clear_position_pb_%d" % self.index)
        self.pump_control_layer3.addWidget(self.clear_position_pb)
        self.stop_pb = QtWidgets.QPushButton(self.centralwidget)
        self.stop_pb.setObjectName("stop_pb_%d" % self.index)
        self.pump_control_layer3.addWidget(self.stop_pb)
        self.addLayout(self.pump_control_layer3)

        self.pump_control_layer4 = QtWidgets.QHBoxLayout()
        self.pump_control_layer4.setObjectName("pump_control_layer4_%d" % self.index)
        self.label_max_speed = QtWidgets.QLabel(self.centralwidget)
        self.label_max_speed.setObjectName("label_max_speed_%d" % self.index)
        self.pump_control_layer4.addWidget(self.label_max_speed)
        self.max_speed = QtWidgets.QSpinBox(self.centralwidget)
        self.max_speed.setMinimum(5)
        self.max_speed.setMaximum(350)
        self.max_speed.setSingleStep(10)
        self.max_speed.setProperty("value", 100)
        self.max_speed.setObjectName("max_speed_%d" % self.index)
        self.pump_control_layer4.addWidget(self.max_speed)
        self.max_speed_pb = QtWidgets.QPushButton(self.centralwidget)
        self.max_speed_pb.setObjectName("max_speed_pb_%d" % self.index)
        self.pump_control_layer4.addWidget(self.max_speed_pb)
        self.addLayout(self.pump_control_layer4)

        self.pump_control_layer5 = QtWidgets.QHBoxLayout()
        self.pump_control_layer5.setObjectName("pump_control_layer5_%d" % self.index)
        self.label_temporary_speed = QtWidgets.QLabel(self.centralwidget)
        self.label_temporary_speed.setObjectName("label_temporary_speed_%d" % self.index)
        self.pump_control_layer5.addWidget(self.label_temporary_speed)
        self.temp_speed = QtWidgets.QSpinBox(self.centralwidget)
        self.temp_speed.setMinimum(1)
        self.temp_speed.setMaximum(350)
        self.temp_speed.setSingleStep(10)
        self.temp_speed.setProperty("value", 200)
        self.temp_speed.setObjectName("temp_speed_%d" % self.index)
        self.pump_control_layer5.addWidget(self.temp_speed)
        self.temp_speed_pb = QtWidgets.QPushButton(self.centralwidget)
        self.temp_speed_pb.setObjectName("temp_speed_pb_%d" % self.index)
        self.pump_control_layer5.addWidget(self.temp_speed_pb)
        self.addLayout(self.pump_control_layer5)

        self.pump_control_layer6 = QtWidgets.QHBoxLayout()
        self.pump_control_layer6.setObjectName("pump_control_layer6_%d" % self.index)
        self.label_suck_volume = QtWidgets.QLabel(self.centralwidget)
        self.label_suck_volume.setObjectName("label_suck_volume_%d" % self.index)
        self.pump_control_layer6.addWidget(self.label_suck_volume)
        self.suck_volume = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.suck_volume.setDecimals(4)
        self.suck_volume.setMaximum(20.0)
        self.suck_volume.setObjectName("suck_volume_%d" % self.index)
        self.pump_control_layer6.addWidget(self.suck_volume)
        self.suck_pb = QtWidgets.QPushButton(self.centralwidget)
        self.suck_pb.setObjectName("suck_pb_%d" % self.index)
        self.pump_control_layer6.addWidget(self.suck_pb)
        self.addLayout(self.pump_control_layer6)

        self.pump_control_layer7 = QtWidgets.QHBoxLayout()
        self.pump_control_layer7.setObjectName("pump_control_layer7_%d" % self.index)
        self.label_discharge_volume = QtWidgets.QLabel(self.centralwidget)
        self.label_discharge_volume.setObjectName("label_discharge_volume_%d" % self.index)
        self.pump_control_layer7.addWidget(self.label_discharge_volume)
        self.discharge_volume = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.discharge_volume.setDecimals(4)
        self.discharge_volume.setMaximum(20.0)
        self.discharge_volume.setObjectName("discharge_volume_%d" % self.index)
        self.pump_control_layer7.addWidget(self.discharge_volume)
        self.discharge_pb = QtWidgets.QPushButton(self.centralwidget)
        self.discharge_pb.setObjectName("discharge_pb_%d" % self.index)
        self.pump_control_layer7.addWidget(self.discharge_pb)
        self.addLayout(self.pump_control_layer7)

        self.pump_control_layer8 = QtWidgets.QHBoxLayout()
        self.pump_control_layer8.setObjectName("pump_control_layer8_%d" % self.index)
        self.label_valve_select = QtWidgets.QLabel(self.centralwidget)
        self.label_valve_select .setObjectName("label_valve_select_%d" % self.index)
        self.pump_control_layer8.addWidget(self.label_valve_select )
        self.valve_id = QtWidgets.QSpinBox(self.centralwidget)
        self.valve_id.setMinimum(1)
        self.valve_id.setMaximum(6)
        self.valve_id.setSingleStep(1)
        self.valve_id.setObjectName("valve_id_%d" % self.index)
        self.pump_control_layer8.addWidget(self.valve_id)
        self.set_valve_pb = QtWidgets.QPushButton(self.centralwidget)
        self.set_valve_pb.setObjectName("set_valve_pb_%d" % self.index)
        self.pump_control_layer8.addWidget(self.set_valve_pb)
        self.pump_control_layer8.addWidget(self.valve_id)
        self.reset_valve_pb = QtWidgets.QPushButton(self.centralwidget)
        self.reset_valve_pb.setObjectName("reset_valve_pb_%d" % self.index)
        self.pump_control_layer8.addWidget(self.reset_valve_pb)
        self.addLayout(self.pump_control_layer8)

        self.pump_control_layer9 = QtWidgets.QHBoxLayout()
        self.pump_control_layer9.setObjectName("pump_control_layer9_%d" % self.index)
        self.current_volume = QtWidgets.QSlider(self.centralwidget)
        self.current_volume.setMaximum(100)
        self.current_volume.setSingleStep(1)
        self.current_volume.setOrientation(QtCore.Qt.Horizontal)
        self.current_volume.setObjectName("current_volume_%d" % self.index)
        self.pump_control_layer9.addWidget(self.current_volume)
        self.read_pos_pb = QtWidgets.QPushButton(self.centralwidget)
        self.read_pos_pb.setObjectName("read_pos_pb_%d" % self.index)
        self.pump_control_layer9.addWidget(self.read_pos_pb)
        self.move_to_pb = QtWidgets.QPushButton(self.centralwidget)
        self.move_to_pb.setObjectName("move_to_pb")
        self.pump_control_layer9.addWidget(self.move_to_pb)
        self.addLayout(self.pump_control_layer9)

        self.send_command_pb.clicked.connect(self.send_command)
        self.reset_pb.clicked.connect(self.reset)
        self.clear_position_pb.clicked.connect(self.clear_position)
        self.stop_pb.clicked.connect(self.stop)
        self.max_speed_pb.clicked.connect(self.set_max_speed)
        self.temp_speed_pb.clicked.connect(self.set_temp_speed)
        self.suck_pb.clicked.connect(self.suck)
        self.discharge_pb.clicked.connect(self.discharge)
        self.read_pos_pb.clicked.connect(self.read_pos)
        self.move_to_pb.clicked.connect(self.move_to)
        self.address.currentIndexChanged['int'].connect(self.update_volume)
        self.set_valve_pb.clicked.connect(self.set_valve)
        self.reset_valve_pb.clicked.connect(self.reset_valve)
        QtCore.QMetaObject.connectSlotsByName(self)

    def get_current_pump_addr(self):
        return int(self.address.currentText())

    def update_volume(self):
        max_volume = self.pump_config[self.address.currentText()]
        self.suck_volume.setMaximum(max_volume)
        self.discharge_volume.setMaximum(max_volume)




    def send_command(self):
        command = self.command.text()
        command_2 = command[2:]
        if (len(command)>0) and (len(command_2)>0) and command.startswith('0x'):
            command = int(command[2:], 16)
        else:
            print('command must start with 0x and after 0x should not be empty. input 0x4b to set speed')
            return False
            # command = int(command)
        param = self.parameter.text()
        if len(param)>0 and is_number(param)==True:
            param = int(self.parameter.text())
        else:
            print("param must be number")
            return False
        # print(self.parameter.text())
        # param = int(self.parameter.text())
        res = self.controller.send_command(self.get_current_pump_addr(), command, param)
        print("%d, 0x%x, %d -> %d"%(self.get_current_pump_addr(), command, param, res))

    def reset(self):
        self.controller.reset(self.get_current_pump_addr())

    def clear_position(self):
        self.controller.reset_position(self.get_current_pump_addr())

    def stop(self):
        self.controller.stop_move(self.get_current_pump_addr())

    def set_max_speed(self):
        self.controller.set_max_speed(self.get_current_pump_addr(), self.max_speed.value())

    def set_temp_speed(self):
        self.controller.set_temporary_speed(self.get_current_pump_addr(), self.temp_speed.value())

    def suck(self):
        self.controller.suck(self.get_current_pump_addr(), self.suck_volume.value())

    def discharge(self):
        self.controller.discharge(self.get_current_pump_addr(), self.discharge_volume.value())

    def read_pos(self):
        addr = self.get_current_pump_addr()
        pos = self.controller.get_current_position(addr)
        max_step = self.controller.volume2step(addr, self.pump_config[str(addr)])
        if pos == -1 or max_step == -1:
            print("Read position failed")
            return
        self.current_volume.setValue(int(pos*self.current_volume.maximum()/max_step))
        print(self.current_volume.setValue(int(pos*self.current_volume.maximum()/max_step)))

    def move_to(self):
        addr = self.get_current_pump_addr()
        self.controller.move_to(addr, self.pump_config[str(addr)]*self.current_volume.value()/self.current_volume.maximum())

    def set_valve(self):
        self.controller.set_valve(self.get_current_pump_addr(), self.valve_id.value())

    def reset_valve(self):
        self.controller.reset_valve(self.get_current_pump_addr())

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_command.setText(_translate("MainWindow", "Command"))
        self.label_parameter.setText(_translate("MainWindow", "Parameter"))
        self.label_address.setText(_translate("MainWindow", "Bump Address"))
        self.send_command_pb.setText(_translate("MainWindow", "Send Command"))
        self.reset_pb.setText(_translate("MainWindow", "Reset"))
        self.clear_position_pb.setText(_translate("MainWindow", "Clear Position"))
        self.stop_pb.setText(_translate("MainWindow", "Stop"))
        self.label_max_speed.setText(_translate("MainWindow", "Max Speed"))
        self.max_speed_pb.setText(_translate("MainWindow", "Set"))
        self.label_temporary_speed.setText(_translate("MainWindow", "Temporary Speed"))
        self.temp_speed_pb.setText(_translate("MainWindow", "Set"))
        self.label_suck_volume.setText(_translate("MainWindow", "Volume"))
        self.suck_pb.setText(_translate("MainWindow", "Suck"))
        self.label_discharge_volume.setText(_translate("MainWindow", "Volume"))
        self.discharge_pb.setText(_translate("MainWindow", "Discharge"))
        self.read_pos_pb.setText(_translate("MainWindow", "Read Position"))
        self.move_to_pb.setText(_translate("MainWindow", "Move"))
        self.label_valve_select.setText(_translate("MainWindow", "Valve ID"))
        self.set_valve_pb.setText(_translate("MainWindow", "Set Valve"))
        self.reset_valve_pb.setText(_translate("MainWindow", "Reset Valve"))


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.controller = zerorpc.Client()
        # self.controller.connect("tcp://10.60.2.122:4242")
        self.controller.connect("tcp://127.0.0.1:4242")

        self.control_units = []
        self.pump_config = self.controller.get_pump_info()
        self.units_per_row = 3
        #self.m_flag = False

        self.setupUi()

        for i in range(len(self.pump_config.keys())):
            self.add_control_unit()

    def add_control_unit(self):
        index = len(self.control_units)
        control_unit = ControlUnit(self, index)
        self.gridLayout.addLayout(control_unit, index//3, index%3, 1, 1)
        self.control_units.append(control_unit)
        control_unit.retranslateUi()
        pumps = sorted(self.pump_config.keys())
        control_unit.address.addItems(pumps)
        if index < len(pumps):
            control_unit.address.setCurrentIndex(index)


    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(352, 290)
        self.setMaximumSize(QtCore.QSize(1600, 1200))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 352, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))


    '''def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))'''




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = Ui_MainWindow()
    my_pyqt_form.show()
    sys.exit(app.exec_())