

from microWebSrv import MicroWebSrv
import henhouse_status as hhstat
from machine import Timer
import pycom
import time
import door
from machine import RTC


def doorcontent():
    (ontime, closetime, status) = hhstat.get()
    now = time.localtime()
    timetxt = hhstat.time2txt(now[3], now[4])
    content = """\
    <!DOCTYPE html>
    <html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>H&oslashnehusd&oslashr&aring;pner</title>
        </head>
        <body>
            <h1>D&oslashra er %s</h1>

            <br />

            <table><tr>
            <td>
                <form action="/open" method="post" accept-charset="ISO-8859-1">
                    <input type="submit" value="Open" maxlength="7"><br />
                </form>
            </td>
            <td>
                <form action="/close" method="post" accept-charset="ISO-8859-1">
                    <input type="submit" value="Close"  maxlength="7"><br />
                </form>
            </td></tr>
            <tr><td>
                <form action="/door" method="post" accept-charset="ISO-8859-1">
                    D&oslash;ra &aringpner: </td><td><input type="text" name="opentime" size="4" value=%s>
            </td></tr>
            <tr><td>
                    D&oslash;ra lukker: </td><td><input type="text" name="closetime" size="4" value=%s>
            </td></tr>
            <tr><td colspan="2">
                    <input type="submit" value="Oppdater tidspunkt">
            </td></tr>
                </form>
                <h2>Time: %s</h2>
        </body>
    </html>
    """ % (hhstat.dor(), ontime, closetime, timetxt)
    return(content)

@MicroWebSrv.route('/door')
def _httpHandlerDoorGet(httpClient, httpResponse) :
    content = doorcontent()
    httpResponse.WriteResponseOk( headers		 = None,
      contentType	 = "text/html",
      contentCharset = "UTF-8",
      content 		 = content )


@MicroWebSrv.route('/close', 'POST')
def _httpHandlerClosePost(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    door.close()
    content   = """\
    <!DOCTYPE html>
    <html lang=en>
    <head>
    <meta charset="UTF-8" />
            <title>Closed!</title>
        </head>
        <body>
            <h1>Closed!</h1>
        </body>
    </html>
    """
    httpResponse.WriteResponseOk( headers		 = None,
      contentType	 = "text/html",
      contentCharset = "UTF-8",
      content 		 = content )

@MicroWebSrv.route('/open', 'POST')
def _httpHandlerOpenPost(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    door.dopen()
    content   = """\
    <!DOCTYPE html>
    <html lang=en>
    <head>
    <meta charset="UTF-8" />
            <title>Open!</title>
        </head>
        <body>
            <h1>Open!</h1>
        </body>
    </html>
    """
    httpResponse.WriteResponseOk( headers		 = None,
      contentType	 = "text/html",
      contentCharset = "UTF-8",
      content 		 = content )


@MicroWebSrv.route('/door', 'POST')
def _httpHandlerDoorPost(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    opentime = formData["opentime"]
    closetime  = formData["closetime"]
    hhstat.updatetime(opentime,closetime)
    #content = doordebug(opentime, closetime)
    content = doorcontent()
    httpResponse.WriteResponseOk( headers		 = None,
      contentType	 = "text/html",
      contentCharset = "UTF-8",
      content 		 = content )



# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg) :
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
    print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
    print("WS CLOSED")

pycom.heartbeat(False)
rtc=RTC()
time.timezone(3600) # Winter time.
alarm = Timer.Alarm(door.timerevent, 30, periodic=True)

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()
