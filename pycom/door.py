
import time
from machine import Pin
import henhouse_status as hhstat
import pycom

def dopen():
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
    '''
    print(hhstat.time2txt(hour, minutes))
    print(hhstat.time2txt(openHour, openMin))
    print(hhstat.time2txt(closeHour, closeMin))
    '''
    if((hour == openHour) and (minutes == openMin)):
        dopen()
    if((hour == closeHour) and (minutes == closeMin)):
        close()

def timerevent(alarm):
    pycom.rgbled(0x0f00)
    time.sleep_ms(10)
    pycom.rgbled(0)
    handler(time.localtime())
