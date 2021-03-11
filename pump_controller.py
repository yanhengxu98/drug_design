import serial
import time
import json
import os
import configure


class Pump(object):
    VOLUME_STEP_MAP = {20: 9600, 10: 9632, 5: 12000, 1: 12000}

    def __init__(self, addr, volume, controller):
        self.addr = addr
        self.controller = controller
        self.max_volume = volume
        self.max_step = self.VOLUME_STEP_MAP[self.max_volume]

        self.SY01 = False
        if self.max_volume == 1:
            self.SY01 = True

    def _send_command(self, cmd, param):
        return self.controller.send_command(self.addr, cmd, param)

    def volume2step(self, volume):
        step = int(volume * self.max_step / self.max_volume)
        return step

    def step2volume(self, step):
        return step * self.max_volume / self.max_step

    def move_to(self, volume):
        current_volume = self.get_current_position()
        if current_volume == -1:
            print("Error during moving, stopped")
            return -1
        current_volume = self.step2volume(current_volume)
        if current_volume > volume:
            return self.discharge(current_volume-volume)
        else:
            return self.suck(volume-current_volume)

    def reset(self):
        return self._send_command(0x45, 0)

    def stop_move(self):
        return self._send_command(0x49, 0)

    def suck(self, volume):
        # self: address of pump.
        # volume: suck volume
        current_pos = self.get_current_position()
        if current_pos == -1:
            print("Error during suck, stopped")
            return -1
        suck_step = min(self.volume2step(volume), self.max_step-current_pos)
        if suck_step == 0:
            return 0
        if self.SY01:
            return self._send_command(0x43, suck_step)
        return self._send_command(0x4d, suck_step)

    def discharge(self, volume):
        # self: address of pump.
        # volume: suck volume
        current_pos = self.get_current_position()
        if current_pos == -1:
            print("Error during discharge, stopped")
            return -1
        discharge_step = min(self.volume2step(volume), current_pos)
        if discharge_step == 0:
            return 0
        return self._send_command(0x42, discharge_step)

    def get_current_position(self):
        return self._send_command(0x66, 0)

    def get_move_direction(self):
        return self._send_command(0x68, 0)

    def reset_position(self):
        return self._send_command(0x67, 0)

    def set_addr(self, new_addr):
        success = self._send_command(0x00, new_addr)
        if success == 0:
            self.controller.update_pump_addr(self.addr, new_addr)
        return success

    def set_baud_rate(self, cmd, baud_rate, param_table):
        if not param_table.get(baud_rate):
            print("Invalid baud rate, support baud rate: %s" % list(param_table.keys()))
            return -1
        return self._send_command(cmd, param_table.get(baud_rate))

    def set_rs_baud_rate(self, cmd, baud_rate):
        return self.set_baud_rate(cmd, baud_rate, {9600: 0x00, 19200: 0x01, 38400: 0x02, 57600: 0x03, 115200: 0x04})

    def set_rs232_baud_rate(self, baud_rate):
        return self.set_baud_rate(0x01, baud_rate)

    def set_rs485_baud_rate(self, baud_rate):
        return self.set_baud_rate(0x02, baud_rate)

    def set_can_baud_rate(self, baud_rate):
        return self.set_baud_rate(0x03, baud_rate, {1e5: 0x00, 2e5: 0x01, 5e5: 0x02, 1e6: 0x03})

    def set_max_speed(self, speed):
        speed = min(max(speed, 5), 350)
        return self._send_command(0x07, speed)

    def set_auto_reset(self, auto_reset):  # True or False
        return self._send_command(0x0e, int(auto_reset))

    def set_can_target_addr(self, addr):
        return self._send_command(0x10, addr)

    def reset_driver_data(self):
        return self._send_command(0xff, 0)

    def get_addr(self):
        return self._send_command(0x20, 0)

    def get_baud_rate(self, cmd, param_table):
        baud_rate = self._send_command(cmd, 0)
        if baud_rate == -1:
            return -1
        return param_table.get(baud_rate)

    def get_rs_baud_rate(self, cmd):
        return self.get_baud_rate(cmd, {0x00: 9600, 0x01: 19200, 0x02: 38400, 0x03: 57600, 0x04: 115200})

    def get_rs232_baud_rate(self):
        return self.get_rs_baud_rate(0x21)

    def get_rs485_baud_rate(self):
        return self.get_rs_baud_rate(0x22)

    def get_can_baud_rate(self):
        return self.get_baud_rate(0x23, {0x00: 1e5, 0x01: 2e5, 0x02: 5e5, 0x03: 1e6})

    def get_max_speed(self):
        speed = self._send_command(0x27, 0)
        if speed == -1:
            return -1
        return speed / 0x015E

    def get_reset_speed(self):
        speed = self._send_command(0x2b, 0)
        if speed == -1:
            return -1
        return speed / 0x015E

    def get_auto_reset(self):
        return self._send_command(0x2e, 0)

    def get_can_target_addr(self):
        return self._send_command(0x30, 0)

    def get_software_version(self):
        return self._send_command(0x3f, 0)

    def get_state(self):
        return self._send_command(0x4a, 0)

    def set_temporary_speed(self, speed):
        # 1 is the max speed
        speed = min(max(speed, 1), 350)
        return self._send_command(0x4b, speed)

    def get_stop_reason(self):
        return self._send_command(0x65, None)

    def set_valve(self, index):
        if not self.SY01:
            return -1
        return self._send_command(0x44, index)

    def reset_valve(self):
        if not self.SY01:
            return -1
        return self._send_command(0x4c, 0)


class SerialController:
    def __init__(self, port=None):
        self.port = self.check_port(port)
        self.open_serial()
        self.PUMPS = {}

        self.config_file = os.path.join(os.path.dirname(__file__), 'pump.config')
        self.ADDR_VOLUME_MAP = self.load_config()

        self.generate_interface()

    def generate_interface(self):
        import inspect
        import operator
        funcs = [i for i in dir(Pump) if inspect.isfunction(getattr(Pump, i)) and not i.startswith('_')]

        def func_maker(func):
            def _(addr, *args):
                opt = operator.methodcaller(func, *args)
                return opt(self.pump(addr))
            return _

        for func in funcs:
            self.__dict__[func] = func_maker(func)

    def get_pump_info(self):
        return self.ADDR_VOLUME_MAP

    def check_port(self, port):
        if not port:
            import serial.tools.list_ports
            ports = [p.device for p in serial.tools.list_ports.comports()]
            print("Avaliable ports:", ports)
            port = input("Please input serial controller port:")
        return port

    def open_serial(self):
        try:
            self.ser = serial.Serial(self.port, 9600)
        except Exception as e:
            print("open serial error", e)
            self.ser = None

    def send_command(self, addr, cmd, param):
        if cmd < 0x11 or cmd == 0xff:  # factory command
            command = bytes([0xCC, addr, cmd, 0xFF, 0xEE, 0xBB, 0xAA, param % 256, param // 256, 0, 0, 0xDD])
        else:
            command = bytes([0xCC, addr, cmd, param % 256, param // 256, 0xDD])
        check_sum = sum(command)
        command += bytes([check_sum % 256, check_sum // 256])

        try:
            self.ser.write(command)
            for i in range(10):
                time.sleep(0.01)
                data = self.ser.read_all()
                if len(data) == 0:
                    continue
                elif len(data) == 8:
                    return self.handle_response_data(cmd, data)
                else:
                    raise Exception("Response data error: %s" % data)
            raise Exception("Wait response time out")

        except Exception as e:
            self.ser.read_all()
            print(command)
            print(e)
            return -1

    def is_query_cmd(self, cmd):
        return cmd // 16 in [2, 3] or cmd in [0x4a, 0x65, 0x66, 0x68]

    def handle_response_data(self, cmd, data):
        if data[0] != 0xCC or data[5] != 0xDD:
            raise Exception("Wrong package head or tail")
        if sum(data[:6]) != data[6] + 256 * data[7]:
            raise Exception("Check sum error")
        if self.is_query_cmd(cmd):
            if cmd == 0x4a:  # query state
                return data[2]
            if data[2] == 0x00:
                return data[3] + data[4] * 256
            raise Exception("Query error: 0x%x" % data[2])
        else:
            if data[2] == 0x00 or data[2] == 0xfe:
                return 0
            elif data[2] == 0x04:
                raise Exception("Pump busy")
            else:
                raise Exception("Control error 0x%x" % data[2])

    def pump(self, addr):
        pump = self.PUMPS.get(addr)
        if pump is None:
            if not self.ADDR_VOLUME_MAP.get(str(addr)):
                print("Unknown volume for Pump%d" % addr)
                return None
            pump = Pump(addr, self.ADDR_VOLUME_MAP.get(str(addr)), self)
            self.PUMPS[addr] = pump
        return pump

    def close(self):
        if self.ser:
            self.ser.close()

    def update_pump_addr(self, old_addr, new_addr):
        pump = self.PUMPS[old_addr]
        pump.addr = new_addr
        self.PUMPS[new_addr] = pump
        del self.PUMPS[old_addr]

        volume = self.ADDR_VOLUME_MAP[str(old_addr)]
        self.ADDR_VOLUME_MAP[str(new_addr)] = volume
        del self.ADDR_VOLUME_MAP[str(old_addr)]

        self.save_config(self.ADDR_VOLUME_MAP)

    def load_config(self):
        
        if not os.path.exists(self.config_file):
            print("Please record the pump configuration in pump.config")
            print('Example config file: {"0":5 ,"1":20}')
            self.save_config({"0": 5, "1": 20})
            return {}
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def save_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f)


