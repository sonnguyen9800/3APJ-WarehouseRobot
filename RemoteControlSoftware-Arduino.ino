#include <SoftwareSerial.h>
SoftwareSerial BTSerial(11, 12); // RX | TX

// Variables from the first joystick 
int VRx = A0;
int VRy = A1;
int xPosition = 0;
int yPosition = 0;

// Variables from the second joystick 
int VRx1 = A2;
int VRy1 = A3;
int xPosition1 = 0;
int yPosition1 = 0;

// Bluetooth state
int State =10;
int checkState = 0;
int btConnected = 9;// Indicated LED if bt is connected

// Auto/Manual mode chaneg
bool modechange = 0;
int mode = 8; // button
bool isAuto = 0;
int Automode = 6; //LED to indicate mode. On if Auto mode.
 
void setup() {
  Serial.begin(9600); 
  BTSerial.begin(9600);
  pinMode(mode, INPUT); 
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(VRx1, INPUT);
  pinMode(VRy1, INPUT);
  pinMode(State,INPUT);
  pinMode(btConnected,OUTPUT);
  pinMode(Automode,OUTPUT);
  digitalWrite(btConnected,LOW);
  digitalWrite(Automode,LOW);
}

void loop() {
  xPosition = analogRead(VRx);
  yPosition = analogRead(VRy);
  xPosition1 = analogRead(VRx1);
  yPosition1 = analogRead(VRy1);
  
  checkState = digitalRead(State);
  isAuto = digitalRead(mode);
  

  Serial.print("X :");
  Serial.println(xPosition);
  Serial.print("Y :");
  Serial.println(yPosition);
  
  // If a button is pressed, mode change
  if(isAuto == 0){
    modechange = !modechange;
    delay (500);
   }

  // If bt is connected 
  if(checkState == 1){
      digitalWrite(btConnected,HIGH);
  }else{
      digitalWrite(btConnected,LOW);
  }

   // If it is auto mode
  if(modechange == 1){
      BTSerial.print('A');
      Serial.println('A');
      digitalWrite(Automode,HIGH);
  } else{
    // Manual mode
    digitalWrite(Automode,LOW);
    if(xPosition < 200 && (yPosition > 200 && yPosition<700)){ // Foward
      BTSerial.print('F');
      Serial.println('F');
    }
    else if((xPosition < 200) && ( yPosition>700)){ // Front Left
      BTSerial.print('b');
      Serial.println('b');
    }
    else if((xPosition > 700) && (yPosition > 200 && yPosition<700)){ // Backward
      BTSerial.print('B');
      Serial.println('B');
    }
    else if((xPosition > 200 && xPosition<700) && yPosition > 700){ // Left
      BTSerial.print('L');
      Serial.println('L');
    }
     else if(xPosition > 700 && yPosition > 700){ // Back Left
      BTSerial.print('8'); 
      Serial.println('8');
    }
    else if(xPosition > 700 && yPosition < 200){// Back Right
      BTSerial.print('5');
      Serial.println('5');
    }
    else if((xPosition > 200 && xPosition<700) &&  yPosition < 500){ // Right
      BTSerial.print('R');
      Serial.println('R');
    }
    else if(xPosition < 200 && yPosition < 200){ // Front Right
      BTSerial.print('2');
      Serial.println('2');
    }
    else if((xPosition1 > 200 && xPosition1<700) && yPosition1 > 700){ // Turning to the left
         BTSerial.print('W');
         Serial.println('W');
     }else if((xPosition1 > 200 && xPosition1<700) &&  yPosition1 < 200){ Turning to the right
       BTSerial.print('C');
        Serial.println('C');
     }else{ // Stop
       BTSerial.print('S');
      Serial.println('S');
    }
  }
 delay(100);
}
