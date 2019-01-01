
import time
from machine import Pin
import henhouse_status as hhstat

def open():
  print("Opening Door")
  hhstat.setdoor('Open')
  openpin = Pin('P23', Pin.OUT)
  openpin.value(1)
  time.sleep_ms(50)
  openpin.value(0)

def close():
  print("Closing Door")
  hhstat.setdoor('Closed')
  closepin = Pin('P22', Pin.OUT)
  closepin.value(1)
  time.sleep_ms(50)
  closepin.value(0)

def handler(now):
    hour = now[3]
    minutes = now[4]

    (ontime, offtime, status) = hhstat.get()
    (openHour, openMin)   = hhstat.txt2time(ontime)
    (closeHour, closeMin) = hhstat.txt2time(offtime)


    if((hour == openHour) and (minutes == openMin)):
        door.open()

    if((hour == closeHour) and (minutes == closeMin)):
        door.close()
