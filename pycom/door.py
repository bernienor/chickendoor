
import time
from machine import Pin
import henhouse_status as hhstat
import pycom

def dopen():
  print("Opening Door")
  hhstat.setdoor1('Open')
  openpin = Pin('P23', Pin.OUT)
  openpin.value(1)
  time.sleep_ms(50)
  openpin.value(0)

def close():
  print("Closing Door")
  hhstat.setdoor1('Closed')
  closepin = Pin('P22', Pin.OUT)
  closepin.value(1)
  time.sleep_ms(50)
  closepin.value(0)

def dopen_2():
  print("Opening Door")
  hhstat.setdoor2('Open')
  openpin = Pin('P21', Pin.OUT)
  openpin.value(1)
  time.sleep_ms(50)
  openpin.value(0)

def close_2():
  print("Closing Door")
  hhstat.setdoor2('Closed')
  closepin = Pin('P20', Pin.OUT)
  closepin.value(1)
  time.sleep_ms(50)
  closepin.value(0)


def handler(now):
    hour = now[3]
    minutes = now[4]

    (ontime, offtime, status, ontime2, offtime2, status2) = hhstat.get()
    (openHour, openMin)   = hhstat.txt2time(ontime)
    (closeHour, closeMin) = hhstat.txt2time(offtime)
    (openHour2, openMin2)   = hhstat.txt2time(ontime2)
    (closeHour2, closeMin2) = hhstat.txt2time(offtime2)
    '''
    print(hhstat.time2txt(hour, minutes))
    print(hhstat.time2txt(openHour, openMin))
    print(hhstat.time2txt(closeHour, closeMin))
    '''
    if((hour == openHour) and (minutes == openMin)):
        dopen()
    if((hour == closeHour) and (minutes == closeMin)):
        close()
    if((hour == openHour2) and (minutes == openMin2)):
        dopen_2()
    if((hour == closeHour2) and (minutes == closeMin2)):
        close_2()

def timerevent(alarm):
    pycom.rgbled(0x0f00)
    time.sleep_ms(10)
    pycom.rgbled(0)
    handler(time.localtime())
