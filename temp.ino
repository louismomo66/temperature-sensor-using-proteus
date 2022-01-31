#include<LiquidCrystal.h>
LiquidCrystal lcd(12,11,5,4,3,2);
int buz = 8;
const int sensor =A0;
float tempC;
float tempf;
float vout;

void setup() {
  // put your setup code here, to run once:
pinMode(sensor,INPUT);
pinMode(buz,OUTPUT);
Serial.begin(9600);
lcd.begin(16,2);
delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
vout =analogRead(sensor);
vout = (vout*500)/1023;
tempC =vout; // Storing value in Celsius
tempf = (vout*1.8)+32; // converting to fahrenheit
if(tempC >=29){
  digitalWrite(buz,HIGH);
  delay(2000);
  digitalWrite(buz,LOW);
}
if(tempC <=24){
  digitalWrite(buz,HIGH);
  delay(1000);
  digitalWrite(buz,LOW);
}
lcd.setCursor(0,0);
lcd.print("In DegreeC = ");
lcd.print(tempC);
lcd.setCursor(0,1);
lcd.print("In Fahrenheit= ");
lcd.print(tempf);
delay(1000);

}
