import serial

from src.core.exception.ArduinoStreamReaderException import ArduinoStreamReaderException
from src.core.port_provider import PortService


class ArduinoData:

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def get_key(self) -> str:
        return self.key

    def get_value(self) -> str:
        return self.value

class ArduinoReceiver:

    def __init__(self, arduino_port_index=0):
        self.arduino_port_listen = PortService().get_arduino_ports()[arduino_port_index] if len(
            PortService().get_arduino_ports()) > 0 else None

    def _check_connection(self, rate=9600) -> bool:
        if self.arduino_port_listen is None: return False
        try:
            testport = serial.Serial(baudrate=rate)
            testport.setDTR(False)
            testport.port = self.arduino_port_listen.get_port_name()
            testport.open()
            return True
        except:
            return False

    def read_stream_data(self, rate=9600) -> list[ArduinoData]:
        if not self._check_connection():
            raise ArduinoStreamReaderException("Connection failed")

        port = serial.Serial(baudrate=rate)
        port.timeout = 2
        port.setDTR(False)
        port.port = self.arduino_port_listen.get_port_name()
        port.open()

        receive_message = port.readline().decode("utf-8").strip()

        if len(receive_message) == 0 or receive_message.count(":") != 2:
            raise ArduinoStreamReaderException("Message is empty or invalid format")

        received_message_parsed = receive_message.split(" ")

        temperature_key = received_message_parsed[0].split(":")[0]
        temperature_value = received_message_parsed[0].split(":")[1]

        humidity_key = received_message_parsed[1].split(":")[0]
        humidity_value = received_message_parsed[1].split(":")[1]

        return [ArduinoData(temperature_key, temperature_value), ArduinoData(humidity_key, humidity_value)]