#include <L298N.h>
#include <QTRSensors.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(0,1);

#define SPEED  250
#define SPEED1  50
#define SPEED_LINE 80
#define rightMaxSpeed 50
#define leftMaxSpeed 50

//BackLeft Motor (LEFT MODULE, OUT3,  OUT4)
#define BR_EN 13
#define BR1 12
#define BR2 11

//FrontRight Motor (correct)
#define FR_EN 10
#define FR1 8
#define FR2 9

//BackRight Motor
#define BL_EN 4
#define BL1 2
#define BL2 3

//FrontLeft(OUT3, OUT4, Right MODULE)
#define FL_EN 7
#define FL1 6
#define FL2 5



L298N backLeft(BL_EN, BL1, BL2);
L298N backRight(BR_EN, BR1, BR2);
L298N frontLeft(FL_EN, FL1, FL2);
L298N frontRight(FR_EN, FR1, FR2);


const char FRONT  =  'F';
const char BACK = 'B';
const char LEFT = 'L';
const char RIGHT = 'R';
const char STOP = 'S';
const char FRONT_RIGHT_225 = '1';
const char FRONT_RIGHT = '2';
const char FRONT_RIGHT_675 = '3';
const char BACK_RIGHT_225 = '4';
const char BACK_RIGHT = '5';
const char BACK_RIGHT_675 = '6';
const char BACK_LEFT_225 = '7';
const char BACK_LEFT = '8';
const char BACK_LEFT_675 = '9';
const char FRONT_LEFT_675 = 'a';
const char FRONT_LEFT = 'b';
const char FRONT_LEFT_225 = 'c';
const char ROTATE_LEFT = 'W';
const char ROTATE_RIGHT = 'C';
const char AUTOMODE = 'A';
const char CONTROLMODE = 'M';




//Constant KP and KD values for PID algorithms of automatic moving robot car
const int KP = 30;
const int KD = 60;
//Normal variables
char BluetoothData;


void goStraight(uint8_t motorSpeed){
        backRight.setSpeed(motorSpeed);
        backLeft.setSpeed(motorSpeed);
        frontRight.setSpeed(motorSpeed);
        frontLeft.setSpeed(motorSpeed);

        backLeft.forward();
        backRight.forward();
        frontLeft.forward();
        frontRight.forward();
}


void goBack(uint8_t motorSpeed){
        backRight.setSpeed(motorSpeed);
        backLeft.setSpeed(motorSpeed);
        frontRight.setSpeed(motorSpeed);
        frontLeft.setSpeed(motorSpeed);

        backLeft.backward();
        backRight.backward();
        frontLeft.backward();
        frontRight.backward();
}

void goLeft(uint8_t motorSpeed){
        backRight.setSpeed(motorSpeed);
        backLeft.setSpeed(motorSpeed);
        frontRight.setSpeed(motorSpeed);
        frontLeft.setSpeed(motorSpeed);

        frontRight.forward();
        backLeft.forward();
        frontLeft.backward();
        backRight.backward();
}

void goRight(uint8_t motorSpeed){
        backRight.setSpeed(motorSpeed);
        backLeft.setSpeed(motorSpeed);
        frontRight.setSpeed(motorSpeed);
        frontLeft.setSpeed(motorSpeed);

        frontRight.backward();
        backLeft.backward();
        frontLeft.forward();
        backRight.forward();

}

void goFrontRight(uint8_t motorSpeed){
        frontLeft.setSpeed(motorSpeed);
        backRight.setSpeed(motorSpeed);
        frontLeft.forward();
        backRight.forward();

}

void goFrontLeft(uint8_t motorSpeed){
        frontRight.setSpeed(motorSpeed);
        backLeft.setSpeed(motorSpeed);
        frontRight.forward();
        backLeft.forward();
}

void goBackLeft(uint8_t motorSpeed){
        frontLeft.setSpeed(motorSpeed);
        backRight.setSpeed(motorSpeed);
        frontLeft.backward();
        backRight.backward();
}

void goBackRight(uint8_t motorSpeed){
        frontRight.setSpeed(motorSpeed);
        backLeft.setSpeed(motorSpeed);
        frontRight.backward();
        backLeft.backward();
}

void stopCar(){
        backLeft.stop();
        backRight.stop();
        frontLeft.stop();
        frontRight.stop();
}

void rotateLeft(uint8_t motorSpeed){
        backRight.setSpeed(motorSpeed);
        backLeft.setSpeed(motorSpeed);
        frontRight.setSpeed(motorSpeed);
        frontLeft.setSpeed(motorSpeed);

        frontRight.forward();
        backRight.forward();
        frontLeft.backward();
        backLeft.backward();
}

void rotateRight(uint8_t motorSpeed){
        backRight.setSpeed(motorSpeed);
        backLeft.setSpeed(motorSpeed);
        frontRight.setSpeed(motorSpeed);
        frontLeft.setSpeed(motorSpeed);

        frontRight.backward();
        backRight.backward();
        frontLeft.forward();
        backLeft.forward();
}

// ###################  Defining the QTR Sensors: BEGIN ######################### //

//line sensors definition
#define NUM_SENSORS 5
#define IR_1 37
#define IR_2 39
#define IR_3 41
#define IR_4 43
#define IR_5 45

//define error values of each infrared sensor when it detects black tape
#define ERR_IR1 -1000
#define ERR_IR2 0
#define ERR_IR3 1000
#define ERR_IR4 2000
#define ERR_IR5 3000

const uint8_t QTR_SENSORS[NUM_SENSORS] = {IR_1, IR_2, IR_3, IR_4, IR_5};
uint16_t sensorValues[NUM_SENSORS];
int lastError = 0;
QTRSensors qtr;
// ###################  Defining the QTR Sensors: END ######################### //

void setup() {
        //  configure the sensors
        qtr.setTypeRC();
        qtr.setSensorPins(QTR_SENSORS, NUM_SENSORS);
        delay(500);

        // 2.5 ms RC read timeout (default) * 10 reads per calibrate() call
        // = ~25 ms per calibrate() call.
        // Call calibrate() 400 times to make calibration take about 10 seconds.
        for (uint16_t i = 0; i < 400; i++) {
                qtr.calibrate();
        }
        // print the calibration minimum values measured when emitters were on
        //  for (uint8_t i = 0; i < NUM_SENSORS; i++)
        //  {
        //    Serial.print(qtr.calibrationOn.minimum[i]);
        //    Serial.print(' ');
        //  }
        //  Serial.println();
        //  for (uint8_t i = 0; i < NUM_SENSORS; i++)
        //  {
        //    Serial.print(qtr.calibrationOn.maximum[i]);
        //    Serial.print(' ');
        //  }

        Serial.begin(9600);
        mySerial.begin(9600);
}

void loop() {


// ######################## AUTO MODE ########################
        //  if(BluetoothData == AUTOMODE){
        // read calibrated sensor values and obtain a measure of the line position
        // from 0 to 5000 (for a white line, use readLineWhite() instead)
        uint16_t position = qtr.readLineBlack(sensorValues);
        int error = position - 1000;
        bool isChangedDirection = false;

        // IR1 - IR2 - IR3 - IR4 - IR5
        // it might help to keep the speeds positive (this is optional)
        // note that you might want to add a similiar line to keep the speeds from exceeding
        // any maximum allowed value
        if ((error == ERR_IR3 && lastError == ERR_IR2) || (error == ERR_IR3 && lastError == ERR_IR3)) { // go straight
                goStraight(SPEED_LINE);
                Serial.println("1");
        } else if (error == ERR_IR2 && lastError == ERR_IR3) { // go left 45 degree
                goFrontLeft(SPEED_LINE);
                Serial.println("2");
                isChangedDirection = true;
        } else if (error == ERR_IR4 && lastError == ERR_IR3) { // go right 45 degree
                goFrontRight(SPEED_LINE);
                Serial.println("3");
                isChangedDirection = true;
        } else if (error == ERR_IR5 && lastError == ERR_IR4) {
                Serial.println("4");
                goFrontRight(SPEED_LINE);
        } else if (error == ERR_IR5 && lastError == ERR_IR1) { // rotate left when all sensors are on the left
                Serial.println("5");
                rotateLeft(SPEED_LINE);
        } else if (error == ERR_IR1 && lastError == ERR_IR5) { // rotate right when all sensors are on the right
                Serial.println("6");
                rotateRight(SPEED_LINE);
        } else if (error <= ERR_IR5 && lastError >= ERR_IR4) {
                Serial.println("7");
                rotateRight(SPEED_LINE);
        } else if (error <= ERR_IR2 && lastError >= ERR_IR1) {
                Serial.println("8");
                rotateLeft(SPEED_LINE);
        } else if (error == ERR_IR5 && !isChangedDirection) {
                Serial.println("9");
                rotateRight(SPEED_LINE);
        } else if (error == ERR_IR1 && !isChangedDirection) {
                Serial.println("10");
                rotateLeft(SPEED_LINE);
        } else if (error == ERR_IR1 || (error >= ERR_IR1 && lastError <= ERR_IR4) || (error >= ERR_IR2 && lastError <= ERR_IR3)) {
                goStraight(SPEED_LINE);
                Serial.println("11");
        }
        lastError = error;
        // ######################################################################################################
        // print the sensor values as numbers from 0 to 1000, where 0 means maximum
        // reflectance and 1000 means minimum reflectance, followed by the line position
//    for (uint8_t i = 0; i < NUM_SENSORS; i++){
//      Serial.print(sensorValues[i]);
//      Serial.print('\t');
//    }
//    Serial.println(position);
//    Serial.print("ERROR:   ");
//    Serial.println(error);
//  } else {
        // ######################## MANUAL CONTROL MODE ########################
//      BluetoothData = Serial.read();
//      if (BluetoothData == FRONT) {
//        goStraight(SPEED);
//      }else if (BluetoothData == BACK) {
//        goBack(SPEED);
//      } else if (BluetoothData == LEFT) {
//        goLeft(SPEED);
//      } else if (BluetoothData == RIGHT) {
//        goRight(SPEED);
//      } else if (BluetoothData ==  FRONT_LEFT) {
//        stopCar();
//        goFrontLeft(SPEED);
//      } else if (BluetoothData ==  FRONT_RIGHT) {
//        stopCar();
//        goFrontRight(SPEED);
//      } else if (BluetoothData ==  BACK_RIGHT) {
//        stopCar();
//        goBackRight(SPEED);
//      } else if (BluetoothData ==  BACK_LEFT) {
//        stopCar();
//        goBackLeft(SPEED);
//      } else if (BluetoothData == ROTATE_LEFT) {
//        rotateLeft(SPEED);
//      } else if (BluetoothData == ROTATE_RIGHT) {
//        rotateRight(SPEED);
//      } else if (BluetoothData == STOP) {
//        stopCar();
//      }
//  }
}
