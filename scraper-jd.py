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
import time, os
from JDWeb import JDWrapper, updateSystemTime

jd = JDWrapper()

def reg_Q(opt):

    #if not jd.login_by_QR():
    #    return
    
    # regular way
    #while not jd.buy(opt) and options.flush:
    #    time.sleep(options.wait / 1000.0)
    n = 0
    # qiang gou
    while n<10 and not jd.regular_qiang(opt):
        time.sleep(250/1000)
        n+=1
    exit()
def lite_Q():
    n = 0
    while n<10 and not jd.oder_submit():
        time.sleep(250/1000)
        n+=1
    exit()

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
                        help='Time of the order to Jing Dong', default='14.08.30')
                
    # synchronize net time
    updateSystemTime()
    # example goods
    ac9 = '3968219'
    k2 = '2615810'
    k2_blue = '4019900'
    k3 = '3959251'
    mi6 = '4099139'
    
    options = parser.parse_args()
    options.time = datetime.combine(date.today(), datetime.strptime(options.time,"%H.%M.%S").time())
    #print('+++++++*******************************+++++++')
    print(options)
  
    # for test
    if options.good == '':
        options.good = mi6
    
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
    print(good_data['link'])
    if jd.pre_add_cart(good_data):
        # 快捷抢购，预先添加购物车
        print("预添加成功！快捷抢购中...")
        sched.add_job(lite_Q,'date', run_date=options.time)
    else:
        # 无法预添加购物车则进行常规抢购
        print("预添加失败！常规抢购中...")
        sched.add_job(reg_Q,'date', run_date=options.time, args=[good_data])
    #sched.print_jobs()
    print('Press Ctrl+{0} to exit'.format('Pause(Break)' if os.name == 'nt' else 'C'))
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown(wait=False)
        print('Exit The Job!')
    else:
        sched.shutdown(wait=True)
    
