#include <Servo.h>

Servo servo1;

const int SERVO_PIN = 9;
const String PING_KEY = "PING";
const String ANGL_KEY = "ANGL";  // Example of data: ANGL<90>
const int MAX_ANGL = 180;
const int MIN_ANGL = 0;

int pos = 90;
int current = 90;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
  servo1.attach(SERVO_PIN);
}

// PING operation for checking connection with application
void pingSerial(String msg) {
  if (msg.equals(PING_KEY)) {
    Serial.println("OK");
  }
}

// ANGLE operation to rotate servo
void angleSerial(String msg) {

  int index = msg.indexOf(ANGL_KEY);
  if (index == 0) {

    // Keys of data
    int startIndex = msg.indexOf('<') + 1;
    int endIndex = msg.indexOf('>');

    // Substract raw data
    if (startIndex != -1 && endIndex != -1 && endIndex > startIndex) {
      String valueStr = msg.substring(startIndex, endIndex);
      int angleValue = valueStr.toInt();

      // Validate income angle value
      if (angleValue > MAX_ANGL) {
        pos = MAX_ANGL;
      } else if (angleValue < MIN_ANGL) {
        pos = MIN_ANGL;
      } else {
        pos = angleValue;
      }
      Serial.println(pos);
    }
  }
}

void rotateServo(long ms) {
  if (pos > current) {
    for (; current <= pos;) {
      servo1.write(current);
      delay(ms);
      current += 1;
    }
  }

  if (pos < current) {
    for (; current >= pos;) {
      servo1.write(current);
      delay(ms);
      current -= 1;
    }
  }
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readString();
    msg.trim();
    pingSerial(msg);
    angleSerial(msg);
  }
  rotateServo(15);
}
