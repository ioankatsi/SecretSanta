#include <Keypad.h>
#include <LiquidCrystal.h>
#include <TM1637Display.h>

// Pins for TM1637 Display
const int CLK = 10;
const int DIO = 12;

// Variables for controlling TM1637 Display without Delay
int numCounter = 500;
int ledState = LOW;  

unsigned long previousMillis = 0;
const long interval = 1000;
bool dot_state = true ;

int PIN[4] ;
int pin_digit = 0 ;

int i = 0;
TM1637Display display(CLK, DIO); //set up the 4-Digit Display.

// print "----" on 4-Digit Display
const uint8_t hi[] = {
  SEG_G ,
  SEG_G ,
  SEG_G ,
  SEG_G ,
};


const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {9, 8, 7, 6}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {5, 4, 3, 2}; //connect to the column pinouts of the keypad

//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){
  Serial.begin(9600);
  delay(2000);
  display.setBrightness(7); //set the diplay to maximum brightness
  display.setSegments(hi);
}
  
void loop(){
    char customKey = customKeypad.getKey();
    
    if (customKey){
      pin_digit++ ;
      Serial.println(customKey);
      PIN[pin_digit] = customKey ;
      if (pin_digit == 4){
        if (PIN[1] == 53 && PIN[2] == 52 && PIN[3] == 51 && PIN[4] == 53) {
          //Serial.print("GOT IT");
          delay(73000);
          //73000
          for(i=0; i<8; i++){
            display.setBrightness(i);
            display.showNumberDecEx(8888, 0b11100000, false, 4, 0);
            delay(250);
            display.clear();            
          }
          while (true){
            char customKey = customKeypad.getKey();
            unsigned long currentMillis = millis();

            if (currentMillis - previousMillis >= interval) {
              // save the last time you changed the output on 4-digit Display
              previousMillis = currentMillis;
          
              // if the LED is off turn it on and vice-versa:
              if (ledState == LOW) {
                ledState = HIGH;     
                if(numCounter%100 > 59){
                  numCounter -= 40;
                }
                 display.showNumberDec(numCounter);
                 numCounter -- ;
              } else {
                ledState = LOW;
                if(numCounter%100 > 59){
                  numCounter -= 40;
                }
                display.showNumberDecEx(numCounter, 0b11100000, false, 4, 0);
                numCounter -- ;
              }
            }
            if (customKey){
               Serial.println(customKey);
              }            
          }
        }
        pin_digit = 0;
          // if Pin is wrong, clear the list
          for (int x = 0; x < sizeof(PIN) / sizeof(PIN[0]); x++){
            PIN[x] = 0; 
          }
        //Serial.println(pin_digit);
      }
    } 
 }
