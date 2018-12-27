import time
import pycom
import door
from machine import RTC


pycom.heartbeat(False)
rtc=RTC()


while True:
  now=rtc.now()
  print(now)

### NB! UTC time!
  if((now[3] == 6) & (now[4] == 15)):
    door.opendoor()
    while(rtc.now()[4] == 0):
      pass
  if((now[3] == 20) & (now[4] == 0)):
    door.closedoor()
    while(rtc.now()[4] == 0):
      pass

  time.sleep_ms(5000)
  pycom.rgbled(0x0f00)
  time.sleep_ms(10)
  pycom.rgbled(0)
