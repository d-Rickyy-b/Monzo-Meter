Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
int ll = D7;

int gotoPos(String pos) {
     myservo.write(pos.toInt());
     return pos.toInt();
 }
 
void setup() 
{ 
  myservo.attach(A4);  //Not all pins are created equal
  pinMode(ll, OUTPUT);
  Spark.function("gotoPos", gotoPos);
} 
 
 
void loop() 
{
}
