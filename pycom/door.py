
import time
from machine import Pin


def opendoor():
  print("Opening Door")
  openpin = Pin('P23', Pin.OUT)
  openpin.value(1)
  time.sleep_ms(50)
  openpin.value(0)

def closedoor():
  print("Closing Door")
  closepin = Pin('P22', Pin.OUT)
  closepin.value(1)
  time.sleep_ms(50)
  closepin.value(0)
