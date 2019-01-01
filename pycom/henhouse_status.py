#
# store and retrive data from file
#

# import henhouse_status as hhstat
#
# hhstat.set('07:00', '21:00', 'Open')
# hhstat.get()
# hhstat.dor()
#
#


def get():
    f = open("henhousestatus.txt", 'r')
    openingtime = f.readline().strip('\n')
    closingtime = f.readline().strip('\n')
    status = f.readline().strip('\n')
    f.close()
    return(openingtime, closingtime, status)


def set(openingtime, closingtime, status):
    f = open("henhousestatus.txt", 'w')
    f.write(openingtime)
    f.write('\n')
    f.write(closingtime)
    f.write('\n')
    f.write(status)
    f.write('\n')
    f.close()


'''
Returns the stored status of the door in Norwegian
'''
def dor():
    if(get()[2] == 'Open'):
        return('&Aring;pen')
    if(get()[2] == 'Closed'):
        return('Lukket')
    return('Ukjent')


def setdoor(stat):
    '''
    Stores the new status of the door, given that the status i either 'Open' or 'Closed'
    '''
    if(stat == 'Open' or stat == 'Close'):
        (ontime, offtime, status) = get()
        set(ontime, offtime, stat)


def updatetime(webuptime, webdowntime):
    '''
    Updates the time as sendt from the web-form. NB! Notice the reformating. This
    ensures clean entries to the statusfile.
    '''
    (u,c,status) = get()
    try:
        uptime   = time2txt(txt2time(webuptime)[0], txt2time(webuptime)[1])
        downtime = time2txt(txt2time(webdowntime)[0], txt2time(webdowntime)[1])
        if((uptime != None) and (downtime != None)):
            set(uptime, downtime, status)
    except:
        pass

def txt2time(text):
    '''
        Converts the givent text to two integers and returns these (hh, mm) if they have
        valid values. Returns None if the values are not valid.
    '''
    '''
        >>> import henhouse_status as hhstat
        >>> webuptime = '07:01'
        >>> hhstat.txt2time(webuptime)
        (7, 1)
        >>> hhstat.time2txt(7, 1)
        '07:01'
    '''
    try:
        num = text.split(':')
        hh=int(num[0])
        mm=int(num[1])
        if(isvalidtime(hh, mm)):
            return(hh, mm)
    except:
        return(None)


def time2txt(hh, mm):
    if(isvalidtime(hh, mm) and isinstance(hh, int) and isinstance(mm, int)) :
        txt = "{:02d}".format(hh) + ":" + "{:02d}".format(mm)
        return(txt)
    else:
        return(None)

def isvalidtime(hh, mm):
    if(hh>=0 and hh<24 and mm>=0 and mm<60):
        return(True)
    return(False)
