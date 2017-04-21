# -*- coding: utf-8 -*-
"""
set system time from any web!
"""

import time
import urllib.request
import urllib.parse
import ctypes


SetSystemTime = ctypes.windll.kernel32.SetSystemTime
GetSystemTime = ctypes.windll.kernel32.GetSystemTime

class SYSTEMTIME(ctypes.Structure):
    c_ushort= ctypes.c_ushort
    _fields_ =  (
                ('wYear', c_ushort), 
                ('wMonth', c_ushort), 
                ('wDayOfWeek', c_ushort), 
                ('wDay', c_ushort), 
                ('wHour', c_ushort), 
                ('wMinute', c_ushort), 
                ('wSecond', c_ushort), 
                ('wMilliseconds', c_ushort), 
                )
    def __str__(self):
        return '%4d%02d%02d%02d%02d%02d.%03d' % (self.wYear,self.wMonth,self.wDay,self.wHour,self.wMinute,self.wSecond,self.wMilliseconds)

def updateSystemTime():
    url= 'http://www.jd.com'
    try:
        response= urllib.request.urlopen(url)
        header= response.info()
        date=header['Date']
        gmt=time.strptime(date[5:25], "%d %b %Y %H:%M:%S")
        st=SYSTEMTIME(gmt.tm_year,gmt.tm_mon,gmt.tm_wday,gmt.tm_mday,gmt.tm_hour,gmt.tm_min,gmt.tm_sec,0)
        SetSystemTime(ctypes.byref(st))
        print('网络校时成功！')
    except Exception as ex:
        print(ex)
        print('网络校时失败')
        return False
    return True
def printCurTime():
    now= time.localtime(time.time())
    print('当前系统时间:', time.strftime("%Y-%m-%d %H:%M:%S", now))
    
if __name__=='__main__':
    printCurTime()
    if updateSystemTime():
        printCurTime()
