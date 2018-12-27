/**
 * @brief controller for chicken-/henhouse door
 * @author Bernt Hustad Hembre
 * 
 * github: https://github.com/bernienor/chickendoor
 * 
 * Resources used:
 * RTC library: https://github.com/Jorropo/ds3231/
 * LCD driver:  https://github.com/iancanada/Arduino-Library-DFRobot-LCD-keypad-shield
 *
 * 
 * I-O:
 * 
 * Buttons (using LCD keypad shield) is using analouge input 0
 * 
 * LCD is using D4-D9
 * 
 * Stepper:
 * out1 D2
 * out2 D3
 * out3 D11
 * out4 D12
 * 
 * RTC: (I2C):
 * 
 * 
 * 
**/

#include<EEPROM.h>
#include "DFR0009.h"
#include <LiquidCrystal.h>

// eeprom helper functions
void store(uint16_t adr, uint16_t value)
{
  EEPROM.write(adr, (value&0xff));
  EEPROM.write(adr+1, value>>8);
}

uint16_t fetch(uint16_t adr)
{
  return(EEPROM.read(adr) + (EEPROM.read(adr+1)<<8));
}

// EEPROM storage positions
#define DONOTUSE 0  // Never use adress 0!
#define TOP_POSITION 4
#define BOTTOM_POSITION 8
#define STORED_POSITION 12


#define STEPS_PR_MOVE 10
#define SCANINTERVAL_MS 10L
#define STEPINTERVAL_US 1000L

#define NOT_SET 0
#define DOOR_CLOSED 1
#define DOOR_OPEN 2

static uint16_t current_position;
static uint16_t set_pos;
static uint8_t door_position;
static uint32_t steppertimer = 0;

void goto_position(uint16_t new_position);
void open_door(void);
void close_door(void);
void move_up(void);
void move_down(void);
void stepp(uint8_t pos);
void stepp_half(uint16_t pos);
void test_movedoor(void);
void debuginfo_2I(uint16_t a, uint16_t b);
void stepper_disengage(void);
void stepper_engage(void);

DFR0009 Key(0);    //analog pin 0 for DFR0009 key pin
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup(void)
{
//  store(TOP_POSITION, 40000);
//  store(BOTTOM_POSITION, 35000);
//  store(STORED_POSITION, 40000);
  
  current_position = fetch(STORED_POSITION);
  goto_position(current_position);  
  door_position = NOT_SET;

  lcd.begin(16, 2);              // start LCD
  lcd.setCursor(0,0);
  lcd.print("Chicken Door");
  pinMode(2, OUTPUT); 
  pinMode(3, OUTPUT); 
  pinMode(11, OUTPUT); 
  pinMode(12, OUTPUT); 
  pinMode(13, OUTPUT); 

//  test_stepper();
//  test_movedoor();

}


void loop()
{
  static uint32_t curtime = 0;
  static uint32_t buttontime = SCANINTERVAL_MS;


  if(curtime < SCANINTERVAL_MS)
    buttontime = SCANINTERVAL_MS; // to ensure rescan after the timer wraps around.
  curtime = millis();

  //Check buttons every 10 ms
  if(buttontime <= curtime) 
  {
    buttontime += SCANINTERVAL_MS;
    switch(Key.read_LCD_buttons())
    {
      case btnRIGHT:
        move_up();
        return;
      case btnUP:
        open_door();
        return;
      case btnDOWN:
        close_door();
        return;
      case btnLEFT:
        move_down();
        return;
      case btnSELECT:
        if(door_position == DOOR_OPEN)
          store(TOP_POSITION, current_position);
        if(door_position == DOOR_CLOSED)
          store(BOTTOM_POSITION, current_position);
      default:
        return;
    }
  }
  
  if(curtime % 500 == 0)  // 
  {
    debuginfo();
  }


/*  if(steppertimer < micros()) 
  {
    steppertimer + micros() + SCANINTERVAL_MS;  
    //debuginfo_2I(steppertimer,micros());
    move_door();
    digitalWrite(13, !digitalRead(13));
  }
*/
//  if(steppertimer > micros()) // Handling wrap around of the micros timer (every ~70 minutes)
//    steppertimer = micros();
    
  delayMicroseconds(STEPINTERVAL_US);
  move_door();

}



void test_movedoor(void)
{
  goto_position( 10000);
  current_position = 0;
  while(1)
  {
    delayMicroseconds(STEPINTERVAL_US);
    move_door();
  }
}


/**
Handles timed movement of the steppers. Must be called at appropriate intervals (stepper time)

**/
void move_door()
{
  if(set_pos == current_position)
  {
    stepper_disengage();
    return;
  } 
  
  stepper_engage();
  if(set_pos > current_position)
    current_position++;
  else
    current_position--;
    
  stepp_half(current_position);
}


void goto_position(uint16_t new_pos)
{
  if(new_pos == 0)
    return;
  set_pos = new_pos;
}


void open_door(void)
{
  goto_position(fetch(TOP_POSITION));
  door_position = DOOR_OPEN;
  store(STORED_POSITION,fetch(TOP_POSITION));
}


void close_door(void)
{
  goto_position(fetch(BOTTOM_POSITION));
  door_position = DOOR_CLOSED;
  store(STORED_POSITION,fetch(BOTTOM_POSITION));
}


void move_up(void)
{
  goto_position(current_position + STEPS_PR_MOVE);
}


void move_down(void)
{
  goto_position(current_position-STEPS_PR_MOVE);
}

/**
Sets the output pins according to the last bits of the pos counter.

The function is set up for full steps.

**/
void stepp(uint8_t pos)
{
  uint8_t out = pos & 0x4;
  digitalWrite(2,  out==0);
  digitalWrite(3,  out==1);
  digitalWrite(11, out==2);
  digitalWrite(12, out==3);
}

/**
Sets the output pins according to the last bits of the pos counter.

The function is set up for half steps.

**/
void stepp_half(uint16_t pos)
{
  uint8_t out = pos & 0x7;

  digitalWrite(2,  (out==0 | out == 1 | out == 7));
  digitalWrite(3,  (out==3 | out == 4 | out == 5));
  digitalWrite(11, (out==1 | out == 2 | out == 3));
  digitalWrite(12, (out==5 | out == 6 | out == 7));
}


void debuginfo(void)
{
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("C:");
    lcd.print(String(current_position, DEC));
    lcd.setCursor(8,0);
    lcd.print("S:");
    lcd.print(String(set_pos, DEC));
    lcd.setCursor(0,1);
    lcd.print("T:");
    lcd.print(String(fetch(TOP_POSITION), DEC));
    lcd.setCursor(8,1);
    lcd.print("B:");    
    lcd.print(String(fetch(BOTTOM_POSITION), DEC));
} 

void debuginfo_2I(uint16_t a, uint16_t b)
{
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("A:");
    lcd.print(String(a, DEC));
    lcd.setCursor(8,0);
    lcd.print("B:");
    lcd.print(String(b, DEC));

}

void alive(String txt)
{
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(txt);
}

void test_stepper(void)
{
  for(int i=0;i<10000;i++)
  {
    delayMicroseconds(1000);
    stepp_half(i);
  }
}

void stepper_disengage(void)
{
  pinMode(2, INPUT); 
  pinMode(3, INPUT); 
  pinMode(11, INPUT); 
  pinMode(12, INPUT); 
}

void stepper_engage(void)
{
  pinMode(2, OUTPUT); 
  pinMode(3, OUTPUT); 
  pinMode(11, OUTPUT); 
  pinMode(12, OUTPUT); 
}
