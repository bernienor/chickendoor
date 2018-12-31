# chickendoor

Controller for opening and closing the door for our chicken/hen house.

One Arduino controls the steppermotor (via a L298N stepper motor driver). It also keeps track of the end positions for the door. This is stored in the EEPROM.

One WiPy module sends trigger signals to the Arduino. Commanding it to open or close the door. The WiPy has a Real Time Clock (synced wia wifi).
