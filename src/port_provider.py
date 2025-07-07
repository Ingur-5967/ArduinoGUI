import serial.tools.list_ports

class Port:
    def __init__(self, port_name: str, description: str, hwid: str):
        self.port_name = port_name
        self.description = description
        self.hwid = hwid

    def get_port_name(self) -> str:
        return self.port_name

    def get_description(self) -> str:
        return self.description

    def get_hwid(self) -> str:
        return self.hwid

class PortService:

    def __init__(self):
       self.ports = serial.tools.list_ports.comports()

    def get_arduino_ports(self) -> list[Port]:
        variable_ports = list(filter(lambda port: ("Arduino" in port.get_description()) or ("USB-SERIAL" in port.get_description()), self.get_port_information()))

        if len(variable_ports) == 0:
            print("No Arduino ports found")
            return list()

        return variable_ports

    def get_port_information(self) -> list[Port]:
        return [Port(port, desc, hwid) for port, desc, hwid in sorted(self.ports)]