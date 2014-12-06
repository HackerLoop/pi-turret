  /*
 ardui turret test
 */


int flywheel = 12;
int trigger= 13;

char buff[1];

void setup() {
  pinMode(flywheel, OUTPUT);
  pinMode(trigger, OUTPUT);
  digitalWrite(flywheel, HIGH);
  digitalWrite(trigger, HIGH);
  
  Serial.begin(9600);
  Serial.setTimeout(424242);
  
  digitalWrite(flywheel, LOW);
}

void loop() {
  /*digitalWrite(flywheel, LOW);
  delay(2000);
  digitalWrite(trigger, LOW);  
  delay(500);
  digitalWrite(trigger, HIGH);
  delay(500);
  digitalWrite(flywheel, HIGH);
  
  delay(6000);*/
 
  Serial.readBytes(buff, sizeof(buff));
  digitalWrite(trigger, LOW);
  delay(150);
  digitalWrite(trigger, HIGH);
}
