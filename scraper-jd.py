# -*- coding: utf-8 -*-

"""
JD online shopping helper tool
-----------------------------------------------------

only support to login by QR code, 
username / password is not working now.

"""

import argparse
#from selenium import webdriver
from datetime import datetime, date
from apscheduler.schedulers.blocking import BlockingScheduler
import time
from JDWeb import JDWrapper, updateSystemTime

jd = JDWrapper()

def main(opt):

    #if not jd.login_by_QR():
    #    return
    
    # regular way
    #while not jd.buy(opt) and options.flush:
    #    time.sleep(options.wait / 1000.0)
        
    # qiang gou
    while not jd.qiang(opt):
        time.sleep(250/1000)


if __name__ == '__main__':
    # help message
    parser = argparse.ArgumentParser(description='Simulate to login Jing Dong, and buy sepecified good')
    #parser.add_argument('-u', '--username', 
    #                    help='Jing Dong login user name', default='')
    #parser.add_argument('-p', '--password', 
    #                    help='Jing Dong login user password', default='')
    parser.add_argument('-a', '--area', 
                        help='Area string, like: 1_72_2799_0 for Beijing', default='5_248_48377_0')    
    parser.add_argument('-g', '--good', 
                        help='Jing Dong good ID', default='')
    parser.add_argument('-c', '--count', type=int, 
                        help='The count to buy', default=1)
    parser.add_argument('-w', '--wait', 
                        type=int, default=1000,
                        help='Flush time interval, unit MS')
    parser.add_argument('-f', '--flush', 
                        action='store_true', 
                        help='Continue flash if good out of stock', default=True)
    parser.add_argument('-s', '--submit', 
                        action='store_true',
                        help='Submit the order to Jing Dong', default=True)
    parser.add_argument('-t', '--time', 
                        help='Time of the order to Jing Dong', default='9.09.59')
                
    # synchronize net time
    updateSystemTime()
    # example goods
    ac9 = '3968219'
    k2 = '2615810'
    k2_blue = '4019900'
    k3 = '3959251'
    mi6 = '4099139'
    
    options = parser.parse_args()
    #print('+++++++*******************************+++++++')
    print(options)
  
    # for test
    if options.good == '':
        options.good = k2_blue
    
    options.time = datetime.combine(date.today(), datetime.strptime(options.time,"%H.%M.%S").time())
    
    '''
    if options.password == '' or options.username == '':
        print u'请输入用户名密码'
        exit(1)
    '''
        
    # longin
    jd.login_by_QR()
    good_data = jd.good_detail(options.good, options.area)
    # time task
    sched = BlockingScheduler()
    sched.add_job(main,'date', run_date=options.time, args=[good_data])
    #sched.print_jobs()
    sched.start()
    #main(options)
    
