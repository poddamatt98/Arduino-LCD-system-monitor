//www.diyusthad.com
#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

char *buffer=NULL;

void checkForSerialMessage()
{
  if (Serial.available() > 0) 
  {
     char bridgeMsg = Serial.read();

     if (bridgeMsg == 'c')
     {
      printCpu(Serial.readStringUntil('s'));
     }
     else if (bridgeMsg == 'g'){
           printGpu(Serial.readStringUntil('s'));

     }
  }
 
}

char * printInt(int integer){
  sprintf(buffer, "%d", integer);
  return buffer;
}

void printCpu(String temp){
  lcd.setCursor(12,0);
  lcd.print(temp);
}

void printGpu(String temp){
  lcd.setCursor(12,1);
  lcd.print(temp);
}

void setup() {
  Serial.begin(9600); // Starts the serial communication
  buffer = (char *) malloc(3*sizeof(char));
  lcd.begin(16, 2);
  lcd.print("CPU:");
  printCpu("null");
  lcd.setCursor(0,1);
  lcd.print("GPU:");
  printGpu("null");  
}

void loop() {
  checkForSerialMessage();
}
