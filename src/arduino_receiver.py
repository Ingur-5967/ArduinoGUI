import serial

import port_provider

class ArduinoData:
    def __init__(self):
        pass

class ArduinoReceiver:

    def __init__(self, arduino_port_index=0):
        self.arduino_port_listen = port_provider.PortService().get_arduino_ports()[arduino_port_index]

    def _check_connection(self, rate=9600) -> bool:
        try:
            serial.Serial(self.arduino_port_listen.get_port_name(), rate)
            return True
        except:
            return False

    def read_stream_data(self, rate=9600) -> ArduinoData:
        if not self._check_connection():
            return ArduinoData()

        port = serial.Serial(self.arduino_port_listen.get_port_name(), rate)

        receive_message = port.readline().decode("utf-8").strip()

        # TODO: Wrapper message (JSON) -> ArduinoData
