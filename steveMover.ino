#include<Servo.h>

Servo head;
Servo l_hand;
Servo r_hand;

// received data
byte val = "";

void setup() {
  // put your setup code here, to run once:
  head.attach(5);
  l_hand.attach(2);
  r_hand.attach(3);

  Serial.begin(9600); // for communicating via serial port with Python
}

void standby(){
  // all motors to these positions
  head.write(90);
  int r_pos = 0;
  int l_pos = 180;
  
  l_hand.write(l_pos);
  r_hand.write(r_pos);
}

void look_left(){
  // rotate hed to left
  head.write(150);
}

void look_right(){
  head.write(30);
}

void no(){
  int i = 0;
  for (i = 0; i < 2; i++){
    head.write(30);
    delay(500);
    head.write(150);
    delay(500);
  }
}

void hands_up(){
  // do this on every command (nothing much just move hands a bit)

  //head.write(150);
  //delay(300);
  //head.write(90);
  
  int i = 0;
  for(i=0; i<= 180; i++){
    int r_pos = i;
    int l_pos = map(r_pos, 0, 180, 180, 0);
  
    l_hand.write(l_pos);
    r_hand.write(r_pos);
    delay(5);
  }

  delay(600);

  for(i=180; i>= 0; i--){
    int r_pos = i;
    int l_pos = map(r_pos, 0, 180, 180, 0);
  
    l_hand.write(l_pos);
    r_hand.write(r_pos);
    delay(5);
  }
  
}

void hi(){

  int i = 0;
  for(i=0; i<= 170; i++){
    r_hand.write(i);
    delay(5);
  }

  for(i=170; i>= 100; i--){
    r_hand.write(i);
    delay(5);
  }

  for(i=100; i<= 170; i++){
    r_hand.write(i);
    delay(5);
  }

  for(i=170; i>= 0; i--){
    r_hand.write(i);
    delay(5);
  }

  standby();
}

void mine(){
  // make right upper-cut
  int i = 0;
  for(i=0; i<= 170; i++){
    int r_pos = i;

    r_hand.write(r_pos);
    delay(5);
  }

  for(int count=0; count<=10; count++){
    int i = 0;
    for(i=170; i>= 60; i--){
      r_hand.write(i);
      delay(1);
      }

    for(i=60; i<= 170; i++){
      r_hand.write(i);
      delay(1);
      }
    }
   standby();
   delay(100);
}

void hand_front(){
  r_hand.write(90);
}

void bailar(){
  for (int i = 0; i < 3; i++){
    l_hand.write(180);
    r_hand.write(170);
    delay(500);
    r_hand.write(0);
    l_hand.write(30);
    delay(500);
  }
}

void loop() {
  standby();
  // put your main code here, to run repeatedly:
  while(Serial.available() > 0)  //look for serial data available or not
  {
    val = Serial.read();        //read the serial value
    if(val == 'l')
    {
      standby();
      look_left();
      delay(1000);
    }
    if(val == 'r')
    {
      standby();
      look_right();
      delay(1000);
    }
    if(val == 'h'){
      // do hi
      hi();
    }
    if(val == 'u'){
      hands_up();
      delay(3000);
    }
    if(val == 'U')
    {
      // uppercut
      mine();
      delay(2000);
    }
    if (val == 'n'){
      no();
    }
    if(val == 'f'){
      hand_front();
      delay(3000);
    }
    if(val == 'b'){
      bailar();
    }
  }
}