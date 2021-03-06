import serial
import time
import serial.tools.list_ports as stl

class stir(object):

    def __init__(self, port):
        self.port = port
        self.open_serial()

        self.speed = 250  # default stirring speed 250 rpm
        self.temperature = 20  # default temp = 20
        self.timer = 0  # default set_timer disable
        # 标志位，标志加热状态
        self.is_heating = 0
        self.is_stirring = 0
        self.setup()
        self.speed = self.read_status()[3]  # 速度是真实速度
        self.temperature = self.read_status()[2] / 10 # 温度是正常的十倍

        self.send_command(bytes([0xFE, 0xA0, 0x00, 0x00, 0x00, 0xA0]))

    def setup(self):
        # 初始化的时候，预先读取一下当前设备信息
        cmd = bytes([0xfe, 0xa1, 0x00, 0x00, 0x00, 0xa1])  # 读取仪器状态，包含校验和
        receive_data = self.send_command(cmd)

        self.is_stirring = not receive_data[3]
        self.is_heating = not receive_data[4]

    def check_port(self, port):
        if not port:
            ports = [p.service for p in stl.comports()]
            print("Avaliable ports:", ports)
            port = input("Please input serial controller port:")
        return port

    def open_serial(self):
        try:
            self.ser = serial.Serial(self.port, 9600)
        except Exception as e:
            print("open serial error", e)
            self.ser = None

    def check_sum(self, cmd):
        check_sum = bytes([sum(cmd[1:]) % 256]) # only remain lower bytes
        return check_sum

    # 这里有很大重构空间
    def send_command(self, cmd):

        try:
            self.ser.write(cmd)
            for i in range(3):
                time.sleep(0.05)
                data = self.ser.read_all()
                if len(data) <= 6:
                    continue
                elif len(data) >= 6:
                    if data[0] != 0xfd:
                        raise Exception("Wrong package head.")
                    if sum(data[1:len(data)-1]) % 256 != data[len(data)-1]:
                        print(data)
                        raise Exception("Check sum error, tail: %s; sum: %s" % (data[len(data)-1], sum(data[:len(data)-1])))
                    else:
                        print(data)
                        return data
                else:
                    raise Exception("Response data error: %s" % data)
            # raise Exception("Wait response time out")

        except Exception as e:
            self.ser.read_all()
            print(cmd)
            print(e)
            return b'\xfd\xa2\x01,\x00\x03\x01\xf4\x01\xb5}'

    def read_status(self):
        cmd = bytes([0xFE, 0xA2, 0x00, 0x00, 0x00])
        cmd += self.check_sum(cmd)
        receive_data = self.send_command(cmd)
        print("Receive OK")

        set_stir = int.from_bytes(receive_data[2:4], 'big')  # 第3，第4字节：设定转速值
        real_stir = int.from_bytes(receive_data[4:6], 'big')  # 第5，第6字节：真实转速值
        set_temp = int.from_bytes(receive_data[6:8], 'big') # 第7，第8字节：设定温度值，是显示温度10倍
        real_temp = int.from_bytes(receive_data[8:10], 'big')   # 第9，第10字节：设定温度值，是显示温度10倍

        print(set_stir)
        print(real_stir)
        print(set_temp)
        print(real_temp)

        return real_temp, real_stir, set_temp, set_stir

    def set_temp_start(self, temp):
        self.temperature = temp
        byte_temp = int(temp * 10).to_bytes(2, 'big')
        # 可重构
        cmd = bytes([0xFE, 0xB2])
        cmd += byte_temp
        cmd += bytes([0x00])
        cmd += self.check_sum(cmd)
        if self.is_heating == 0:
            send_data = self.send_command(cmd)
            self.is_heating = 1
        else:
            send_data = self.send_command(cmd)  # 如果本来就开着，重设温度需要发送两次
            send_data = self.send_command(cmd)
        return send_data

    def heat_off(self, temp):
        '''
        首先判断加热器是否是开的状态，是的话才发送关闭命令（设定的温度不会变），否则直接return
        :return: None
        '''
        if self.is_heating == 0:
            return 0
        else:
            self.temperature = temp
            byte_temp = int(temp * 10).to_bytes(2, 'big')
            cmd = bytes([0xFE, 0xB2])
            cmd += byte_temp
            cmd += bytes([0x00])
            cmd += self.check_sum(cmd)
            send_data = self.send_command(cmd)
            self.is_heating = 0
            return send_data

    def set_stir_start(self, speed):
        '''
        按照通讯协议组装改转速代码，发送出去
        :param speed: 期望转速
        :return: 发送的命令x16编码
        '''
        self.speed = speed
        byte_speed = int(speed).to_bytes(2, 'big')
        cmd = bytes([0xFE, 0xB1])
        cmd += byte_speed
        cmd += bytes([0x00])
        cmd += self.check_sum(cmd)
        if self.is_stirring == 0:
            send_data = self.send_command(cmd)
            self.is_stirring = 1
        else:
            send_data = self.send_command(cmd)
            send_data = self.send_command(cmd)
        return send_data

    def stir_off(self, speed):
        '''
        首先判断搅拌器是否是开的状态，是的话才发送关闭命令（设定的转速不会变），否则直接return
        :return: None
        '''
        if self.is_stirring == 0:
            return 0
        else:
            self.speed = speed
            byte_speed = int(speed).to_bytes(2, 'big')
            cmd = bytes([0xFE, 0xB1])
            cmd += byte_speed
            cmd += bytes([0x00])
            cmd += self.check_sum(cmd)
            send_data = self.send_command(cmd)
            self.is_stirring = 0
            return send_data


if __name__ == "__main__":
    stirrer = stir("com4")
    stirrer.read_status()
    stirrer.set_temp_start(40)
    time.sleep(10)
    stirrer.heat_off(10)

