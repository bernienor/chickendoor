/**
 * @file DFR0009.h
 * head file of DFR0009 class
 * Copyright (C) Ian Jin 
 * iancanada.mail@gmail.com
 * https://github.com/iancanada
 * Twitter: @iancanadaTT
 * 
 * 2015-08-26 First release Ver1.00
 * 
 * This program is free software: you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by the
 * Free Software Foundation, either version 3 of the License, or any later
 * version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
 * for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef DRF0009_H_
#define DRF0009_H_

#include <arduino.h>

typedef enum
{
  btnCLR=0,
  btnNONE,
  btnRIGHT,
  btnUP,     
  btnDOWN,   
  btnLEFT,  
  btnSELECT,   
} button_t;

typedef enum
{
  WAITCHANGE=0,
  CHANGED,    
} DFR0009State_t;

class DFR0009
{
  int pin;
  button_t currentKey,changedKey,flag;
  DFR0009State_t state;    
  
public:

  DFR0009(int analogPin);
  void scan();
  button_t getflag();
  button_t read_LCD_buttons();
};

#endif
