# -*- coding: utf-8 -*-

"""
JD online shopping helper tool
-----------------------------------------------------

only support to login by QR code, 
username / password is not working now.

"""

import argparse
#from selenium import webdriver
from datetime import datetime, date, time
from apscheduler.schedulers.blocking import BlockingScheduler

from JDWeb import JDWrapper

jd = JDWrapper()

def main(options):

    #if not jd.login_by_QR():
    #    return

    while not jd.buy(options) and options.flush:
        time.sleep(options.wait / 1000.0)


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
                        type=int, default=500,
                        help='Flush time interval, unit MS')
    parser.add_argument('-f', '--flush', 
                        action='store_true', 
                        help='Continue flash if good out of stock', default=True)
    parser.add_argument('-s', '--submit', 
                        action='store_true',
                        help='Submit the order to Jing Dong', default=True)
                
    # example goods
    hw_watch = '2567304'
    ac9 = '3968219'
    k2_blue = '4019900'
    
    options = parser.parse_args()
    #print('+++++++*******************************+++++++')
    print(options)
  
    # for test
    if options.good == '':
        options.good = k2_blue
    
    '''
    if options.password == '' or options.username == '':
        print u'请输入用户名密码'
        exit(1)
    '''
    # longin
    jd.login_by_QR()
    # time task
    sched = BlockingScheduler()
    sched.add_job(main,'date', run_date=datetime.combine(date.today(), time(9,59,59)), args=[options])
    sched.start()
    #main(options)
    
