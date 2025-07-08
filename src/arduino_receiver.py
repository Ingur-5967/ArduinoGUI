from typing import List

import serial

import port_provider

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
        self.arduino_port_listen = port_provider.PortService().get_arduino_ports()[arduino_port_index] if len(port_provider.PortService().get_arduino_ports()) > 0 else None

    def _check_connection(self, rate=9600) -> bool:
        if self.arduino_port_listen is None: return False

        try:
            serial.Serial(self.arduino_port_listen.get_port_name(), rate)
            return True
        except:
            return False

    def read_stream_data(self, rate=9600) -> list[None] | list[ArduinoData]:
        if not self._check_connection():
            return [None] * 2

        port = serial.Serial(self.arduino_port_listen.get_port_name(), rate)

        receive_message = port.readline().decode("utf-8").strip()

        received_message_parsed = receive_message.split(" ")

        temperature_key = received_message_parsed[0].split(":")[0]
        temperature_value = received_message_parsed[0].split(":")[1]

        humidity_key = received_message_parsed[0].split(":")[0]
        humidity_value = received_message_parsed[0].split(":")[1]

        print(temperature_key, temperature_value, humidity_key, humidity_value)

        return [ArduinoData(temperature_key, temperature_value), ArduinoData(humidity_key, humidity_value)]