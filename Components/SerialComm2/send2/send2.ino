

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

const byte numChars = 100;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

boolean newData = false;

unsigned int incoming[6] = {0, 0, 0, 0, 0, 0};

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  servo1.attach(3); // attaches the servo on pin _ to the servo object
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(9);
  servo5.attach(11);

  servo1.write(0); //thumb has max of 160
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
  servo5.write(0);
}

void loop() {
  recvWithStartEndMarkers();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    // this temporary copy is necessary to protect the original data
    //   because strtok() used in parseData() replaces the commas with \0
    parseData();
    servoWrite();
    newData = false;
  }
}
void servoWrite() {
  if (incoming[0] == 255)
  {
    pos1 = incoming[1];
    pos2 = incoming[2];
    pos3 = incoming[3];
    pos4 = incoming[4];
    pos5 = incoming[5];
  }

  for (int j = 0; j < 6; j++)
  {
    Serial.print(incoming[j]);
  }

  if (pos1 >= 0 && pos1 <= 180)
  {
    servo1.write(pos1);// the servo will move according to position
    //delay(15);//delay for the servo to get to the position
  }
  if (pos2 >= 0 && pos2 <= 180)
  {
    servo2.write(pos2);// the servo will move according to position
    //delay(15);//delay for the servo to get to the position
  }
  if (pos3 >= 0 && pos3 <= 180)
  {
    servo3.write(pos3);// the servo will move according to position
    //delay(15);//delay for the servo to get to the position
  }
  if (pos4 >= 0 && pos4 <= 180)
  {
    servo4.write(pos4);// the servo will move according to position
    //delay(15);//delay for the servo to get to the position
  }
  if (pos5 >= 0 && pos5 <= 180)
  {
    servo5.write(pos5);// the servo will move according to position
    //delay(15);//delay for the servo to get to the position
  }

}

void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}

//============

void parseData() {      // split the data into its parts

  char * strtokIndx; // this is used by strtok() as an index

  //idk why but a for loop doesn't work here
  strtokIndx = strtok(tempChars, ",");     // get the first part - the string
  incoming[0] = atoi(strtokIndx); // copy it to incoming array

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  incoming[1] = atoi(strtokIndx);     // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  incoming[2] = atoi(strtokIndx);     // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  incoming[3] = atoi(strtokIndx);     // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  incoming[4] = atoi(strtokIndx);     // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  incoming[5] = atoi(strtokIndx);     // convert this part to an integer

}
