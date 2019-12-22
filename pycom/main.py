

from microWebSrv import MicroWebSrv
import henhouse_status as hhstat
from machine import Timer
import pycom
import time
import door
from machine import RTC


def doorcontent():
    (ontime1, closetime1, status1, ontime2, closetime2, status2) = hhstat.get()
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
                <form action="/open_inner" method="post" accept-charset="ISO-8859-1">
                    <input type="submit" value="&Aring;pne indre" maxlength="7"><br />
                </form>
            </td>
            <td>
                <form action="/close_inner" method="post" accept-charset="ISO-8859-1">
                    <input type="submit" value="Lukke indre"  maxlength="7"><br />
                </form>
            </td>
            <td>
                <form action="/open_outer" method="post" accept-charset="ISO-8859-1">
                    <input type="submit" value="&Aring;pne ytre" maxlength="7"><br />
                </form>
            </td>
            <td>
                <form action="/close_outer" method="post" accept-charset="ISO-8859-1">
                    <input type="submit" value="Lukke ytre"  maxlength="7"><br />
                </form>
            </td>
            </tr>
            <tr>
             <td> <form action="/door" method="post" accept-charset="ISO-8859-1">
                  D&oslash;ra &aringpner: </td>
             <td> <input type="text" name="opentime1" size="4" value=%s> </td>
            </tr>
            <tr>
             <td> D&oslash;ra lukker: </td>
             <td><input type="text" name="closetime1" size="4" value=%s> </td>
            </tr>
            <tr>
             <td>
                  D&oslash;ra &aringpner: </td>
             <td> <input type="text" name="opentime2" size="4" value=%s> </td>
            </tr>
            <tr>
             <td> D&oslash;ra lukker: </td>
             <td><input type="text" name="closetime2" size="4" value=%s> </td>
            </tr>
            <tr>
             <td colspan="2">
                    <input type="submit" value="Oppdater tidspunkt">
             </td>
            </tr>
                </form>
                <h2>Time: %s</h2>
        </body>
    </html>
    """ % (hhstat.dor(), ontime1, closetime1, ontime2, closetime2, timetxt)
    return(content)

@MicroWebSrv.route('/door')
def _httpHandlerDoorGet(httpClient, httpResponse) :
    content = doorcontent()
    httpResponse.WriteResponseOk( headers		 = None,
      contentType	 = "text/html",
      contentCharset = "UTF-8",
      content 		 = content )


@MicroWebSrv.route('/close_inner', 'POST')
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

@MicroWebSrv.route('/open_inner', 'POST')
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

@MicroWebSrv.route('/close_outer', 'POST')
def _httpHandlerClosePost(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    door.close_2()
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

@MicroWebSrv.route('/open_outer', 'POST')
def _httpHandlerOpenPost(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    door.dopen_2()
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
    opentime1 = formData["opentime1"]
    closetime1  = formData["closetime1"]
    opentime2 = formData["opentime2"]
    closetime2  = formData["closetime2"]

    hhstat.updatetime(opentime1, closetime1, opentime2, closetime2)
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

#hhstat.set("08:00", "19:30", "Open", "08:00", "19:30", "Open")
pycom.heartbeat(False)
rtc=RTC()
time.timezone(3600) # Winter time.
alarm = Timer.Alarm(door.timerevent, 30, periodic=True)

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()
