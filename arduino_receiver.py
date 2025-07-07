import serial

def read_value(com_port: str, cooldown: int):
    ser = serial.Serial(com_port, cooldown)
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
        except Exception as e:
            print("Ошибка при чтении:", e)