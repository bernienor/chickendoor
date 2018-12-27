# Boot.py for NHSW and serial config
from machine import UART
from machine import RTC
from machine import Pin
#
# The mywifi.py file contains two variables, and looks a bit like this:
# ssid = "MYSSID"
# pwd  = "ThePassWordForMyWifiNetwork"
#
import mywifi

uart = UART(0, 115200)
os.dupterm(uart)

# Switching to external antenna
Pin('P12', mode=Pin.OUT)(True)

from network import WLAN
wlan = WLAN(mode=WLAN.STA)
wlan.scan()

wlan.connect(ssid=mywifi.ssid, auth=(WLAN.WPA2, mywifi.pwd))
while not wlan.isconnected():
  pass
print(wlan.ifconfig())

rtc=RTC()
rtc.ntp_sync('no.pool.ntp.org')
