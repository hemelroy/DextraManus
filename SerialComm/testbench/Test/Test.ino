//GUIDE: https://www.instructables.com/Controlling-Servo-motor-using-Keyboard-input/
//NEED TO SET UP SERIAL COMM WITH ARDUINO USING TERA TERM SOFTWARE
//SERVO1, Q = ANTICLOCKWISE, W = CLOCKWISE
//SERVO2, E = ANTICLOCKWISE, R = CLOCKWISE
//SERVO3, T = ANTICLOCKWISE, Y = CLOCKWISE
//SERVO4, U = ANTICLOCKWISE, I = CLOCKWISE
//SERVO5, O = ANTICLOCKWISE, P = CLOCKWISE

#include <Servo.h>

Servo servo1; // create servo object to control a servo
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

int pos1 = 90;    // variable to store the servo position
int pos2 = 90;
int pos3 = 90;
int pos4 = 90;
int pos5 = 90;

int val; // initial value of input

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600); // Serial comm begin at 9600bps

  // Attach the Servo variable to a pin. Note that in Arduino 0016 and earlier, the Servo library supports servos on only two pins: 9 and 10.
  // Should be a PWM pin, digital pins is unreliable.

  servo1.attach(10); // attaches the servo on pin _ to the servo object
  servo2.attach(3);
  servo3.attach(5);
  servo4.attach(6);
  servo5.attach(9);

}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available()) // if serial value is available
  {
    val = Serial.read();// then read the serial value

    //SERVO1, Q = ANTICLOCKWISE, W = CLOCKWISE
    if (val == 'q') //if value input is equals to q
    {
      if (pos1 >= 0 && pos1 < 180)
      {
        pos1 += 5; //than position of servo motor increases by 1 ( anti clockwise)
        servo1.write(pos1);// the servo will move according to position
        delay(15);//delay for the servo to get to the position
      }
    }
    if (val == 'w') //if value input is equals to w
    {
      if (pos1 > 0 && pos1 <= 180)
      {
        pos1 -= 5; //than position of servo motor decreases by 1 (clockwise)
        servo1.write(pos1);// the servo will move according to position
        delay(15);//delay for the servo to get to the position
      }
    }

    //SERVO2, E = ANTICLOCKWISE, R = CLOCKWISE
    if (val == 'e')
    {
      if (pos2 >= 0 && pos2 < 180)
      {
        pos2 += 5;
        servo2.write(pos2);
        delay(15);
      }
    }
    if (val == 'r')
    {
      if (pos2 > 0 && pos2 <= 180)
      {
        pos2 -= 5;
        servo2.write(pos2);
        delay(15);
      }
    }

    //SERVO3, T = ANTICLOCKWISE, Y = CLOCKWISE
    if (val == 't')
    {
      if (pos3 >= 0 && pos3 < 180)
      {
        pos3 += 5;
        servo3.write(pos3);
        delay(15);
      }
    }
    if (val == 'y')
    {
      if (pos3 > 0 && pos3 <= 180)
      {
        pos3 -= 5;
        servo3.write(pos3);
        delay(15);
      }
    }


    //SERVO4, U = ANTICLOCKWISE, I = CLOCKWISE
    if (val == 'u')
    {
      if (pos4 >= 0 && pos4 < 180)
      {
        pos4 += 5;
        servo4.write(pos4);
        delay(15);
      }
    }
    if (val == 'i')
    {
      if (pos4 > 0 && pos4 <= 180)
      {
        pos4 -= 5;
        servo4.write(pos4);
        delay(15);
      }
    }


    //SERVO5, O = ANTICLOCKWISE, P = CLOCKWISE
    if (val == 'o')
    {
      if (pos5 >= 0 && pos5 < 180)
      {
        pos5 += 5;
        servo5.write(pos5);
        delay(15);
      }
    }
    if (val == 'p')
    {
      if (pos5 > 0 && pos5 <= 180)
      {
        pos5 -= 5;
        servo5.write(pos5);
        delay(15);
      }
    }

    Serial.println((String)"S1: " + pos1);
    Serial.println((String)"S2: " + pos2);
    Serial.println((String)"S3: " + pos3);
    Serial.println((String)"S4: " + pos4);
    Serial.println((String)"S5: " + pos5 + "\n");
  }
}
