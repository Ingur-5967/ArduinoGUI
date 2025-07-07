import serial

def check_variable_port_to_read(com_port: str):
    try:
        serial.Serial(com_port, 9600)
        return True
    except Exception:
        return False

def read_stream_data(com_port: str, rate: int):
    port = serial.Serial(com_port, rate)

    if not check_variable_port_to_read(com_port):
        return None

    return port.readline().decode("utf-8").strip()