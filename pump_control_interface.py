import zerorpc
from pump_controller import SerialController

# configure pump controller here.
controller = SerialController('com9')

s = zerorpc.Server(controller)

s.bind("tcp://0.0.0.0:4242")

try:
    s.run()
    print("Running ...")
except KeyboardInterrupt:
    s.close()
    controller.close()
    print("Exiting ...")
    exit()

