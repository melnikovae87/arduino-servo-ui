![app_cover.png](assets/iot.ico)

# UI Arduino Servo Control

### Release 1.0 _(30.05.2024)_

- [ArduinoUI for MacOS](https://github.com/melnikovae87/arduino-servo-ui/releases/download/1.0/ArduinoUI_Mac.zip)
- [ArduinoUI for Windows](https://github.com/melnikovae87/arduino-servo-ui/releases/download/1.0/ArduinoUI_Win.zip)
- [Arduino Code](https://github.com/melnikovae87/arduino-servo-ui/releases/download/1.0/serial_com.zip)

### Specification

```text
MODEL = Arduino UNO/NANO
DIGITAL_PIN = 9
TYPE = PWM
SERIAL_BAUD_RATE = 9600
SERIAL_PORT = by default detect Arduino device

Communication keys:
PING - check RX/TX communication
ANGL<90> - set servo angle for connected device
```

### Arduino Code for upload

1. Open **Arduino IDE** (from v.2.3.2)
2. Open with IDE folder **libs/serial_com**
3. Connect **PIN #9** to communication wire (yellow) with Servo (VCC and GND optional)
4. Connect Arduino UNO/NANO and UPLOAD code
5. **IMPORTANT**: do not open **Serial Monitor** in IDE (allowed only one connection to Serial Port on OS Win/Linux)

### [Build EXE file script](https://pyinstaller.org/en/stable/usage.html)

```shell
pyinstaller main.py \
  --clean \
  --onefile \
  --windowed \
  --icon=assets/iot.ico \
  --name ArduinoUI
```


