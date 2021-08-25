import serial
arduino = serial.Serial(port='/dev/cu.SLAB_USBtoUART',
                        baudrate=1000000)
x = []
try:
    while True:
        try:
            xs = list(map(int, arduino.readline().decode(
                'utf-8').strip().split(';')))
            # print(xs)
            x.append(xs)
        except TypeError:
            pass
        except ValueError:
            pass
except KeyboardInterrupt:
    print(x)
