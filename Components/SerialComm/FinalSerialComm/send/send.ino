

#include <Servo.h>

Servo servo1; // create servo object to control a servo
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

int pos1 = 0;    // variable to store the servo position
int pos2 = 0;
int pos3 = 0;
int pos4 = 0;
int pos5 = 0;

unsigned int incoming[6] = {0, 0, 0, 0, 0, 0};

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  servo1.attach(10); // attaches the servo on pin _ to the servo object
  servo2.attach(3);
  servo3.attach(5);
  servo4.attach(6);
  servo5.attach(9);
}
void loop() {
  while (!Serial.available());
  incoming[0] = Serial.readString().toInt();

  if (incoming[0] == 255)
  {
    for (int i = 1; i < 5; i++)
    {
      while (!Serial.available());
      incoming[i] = Serial.readString().toInt();
    }
    pos1 = incoming[1];
    pos2 = incoming[2];
    pos3 = incoming[3];
    pos4 = incoming[4];
    pos5 = incoming[5];
  }

  if (pos1 >= 0 && pos1 <= 180)
  {
    servo1.write(pos1);// the servo will move according to position
    delay(15);//delay for the servo to get to the position
  }
  if (pos2 >= 0 && pos2 <= 180)
  {
    servo2.write(pos2);// the servo will move according to position
    delay(15);//delay for the servo to get to the position
  }
  if (pos3 >= 0 && pos3 <= 180)
  {
    servo3.write(pos3);// the servo will move according to position
    delay(15);//delay for the servo to get to the position
  }
  if (pos4 >= 0 && pos4 <= 180)
  {
    servo4.write(pos4);// the servo will move according to position
    delay(15);//delay for the servo to get to the position
  }
  if (pos5 >= 0 && pos5 <= 180)
  {
    servo5.write(pos5);// the servo will move according to position
    delay(15);//delay for the servo to get to the position
  }
}
