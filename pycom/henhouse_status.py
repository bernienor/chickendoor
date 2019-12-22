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
    openingtime1 = f.readline().strip('\n')
    closingtime1 = f.readline().strip('\n')
    status1 = f.readline().strip('\n')
    openingtime2 = f.readline().strip('\n')
    closingtime2 = f.readline().strip('\n')
    status2 = f.readline().strip('\n')
    f.close()
    return(openingtime1, closingtime1, status1, openingtime2, closingtime2, status2)



def set(openingtime1, closingtime1, status1, openingtime2, closingtime2, status2):
    f = open("henhousestatus.txt", 'w')
    f.write(openingtime1)
    f.write('\n')
    f.write(closingtime1)
    f.write('\n')
    f.write(status1)
    f.write('\n')
    f.write(openingtime2)
    f.write('\n')
    f.write(closingtime2)
    f.write('\n')
    f.write(status2)
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

'''
Returns the stored status of the door in Norwegian
'''
def dor2():
    if(get()[5] == 'Open'):
        return('&Aring;pen')
    if(get()[5] == 'Closed'):
        return('Lukket')
    return('Ukjent')

def setdoor1(stat):
    '''
    Stores the new status of the door, given that the status i either 'Open' or 'Closed'
    '''
    if(stat == 'Open' or stat == 'Closed'):
        (ontime, offtime, status , a, b, c) = get()
        set(ontime, offtime, stat, a, b, c)

def setdoor2(stat):
    '''
    Stores the new status of the door, given that the status i either 'Open' or 'Closed'
    '''
    if(stat == 'Open' or stat == 'Closed'):
        (a, b, c, ontime, offtime, status) = get()
        set(a, b, c, ontime, offtime, stat)

def updatetime(webuptime, webdowntime,webuptime2, webdowntime2):
    '''
    Updates the time as sendt from the web-form. NB! Notice the reformating. This
    ensures clean entries to the statusfile.
    '''
    (u,c,status, u2,c2,status2) = get()
    try:
        uptime    = time2txt(txt2time(webuptime)[0], txt2time(webuptime)[1])
        downtime  = time2txt(txt2time(webdowntime)[0], txt2time(webdowntime)[1])
        uptime2   = time2txt(txt2time(webuptime2)[0], txt2time(webuptime2)[1])
        downtime2 = time2txt(txt2time(webdowntime2)[0], txt2time(webdowntime2)[1])
        #print(uptime, downtime, uptime2, downtime2)
        if((uptime != None) and (downtime != None)):
            set(uptime, downtime, status, uptime2, downtime2, status2)
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
