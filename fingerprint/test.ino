String(InBytes);
const int ledpin = 5;
void setup(){
  // put your setup code here, to run once:
Serial.begin(9600);

pinMode(ledpin,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
if (Serial.available()>0){
  InBytes = Serial.readStringUntil('\n');
  if (InBytes == "on"){
    digitalWrite(ledpin,HIGH);
    Serial.write("mandeha");
  }
  if (InBytes == "off"){
    digitalWrite(ledpin,LOW);
    Serial.write("maty");
  }  
   
 
  
}
}
