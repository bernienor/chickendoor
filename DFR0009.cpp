/**
 * @file DFR0009.h
 * implementation file of DFR0009 class
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
#include "DFR0009.h"

DFR0009::DFR0009(int analogPin)
{
  pin=analogPin;
  currentKey=btnNONE;
  changedKey=btnNONE;
  flag=btnCLR;
  state=WAITCHANGE;
}

void DFR0009::scan()
{
  switch(state)
  {
    case WAITCHANGE:
      changedKey=read_LCD_buttons();
      if(changedKey!=currentKey)
        state=CHANGED;
      break;
    
    case CHANGED:
      if(read_LCD_buttons()==changedKey)  //key change confimed 
      {
        currentKey=changedKey;            //update currentKEY
        flag=changedKey;                  //set flag in this case
      }
      state=WAITCHANGE;                   //no matter what, next state will be WAITCHANGE
      break;
      
    default:                              //in any case, back to WAITCHANGE state as default
      state=WAITCHANGE;                   
      break;         
  }    
}

button_t DFR0009::getflag()
{
  button_t flagToReturn;
  
  flagToReturn=flag;
  flag=btnCLR;        //clear flag automatically when get
  return(flagToReturn);  
}

//this function was revised from DFR0009 example code
button_t DFR0009::read_LCD_buttons()
{
  int adc_key_in;
  adc_key_in = analogRead(pin);      // read the value from the sensor 
  // my buttons when read are centered at these valies: 0, 144, 329, 504, 741
  // we add approx 50 to those values and check to see if we are close
  if (adc_key_in > 1000) return btnNONE; // We make this the 1st option for speed reasons since it will be the most likely result
  // For V1.1 us this threshold
  if (adc_key_in < 50)   return btnRIGHT;  
  if (adc_key_in < 250)  return btnUP; 
  if (adc_key_in < 450)  return btnDOWN; 
  if (adc_key_in < 650)  return btnLEFT; 
  if (adc_key_in < 850)  return btnSELECT;  
  return btnNONE;  // when all others fail, return this...  
}
 

