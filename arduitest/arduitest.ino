/*
 ardui turret test
 */


int flywheel = 12;
int trigger= 13

void setup() {
  pinMode(flywheel, OUTPUT);
  pinMode(trigger, OUTPUT);
}

void loop() {
  digitalWrite(flywheel, HIGH);
  delay(500);               
  digitalWrite(trigger, HIGH);  
  delay(300);
  digitalWrite(flywheel, LOW);
  digitalWrite(trigger, LOW);
  delay(10000);  
}
