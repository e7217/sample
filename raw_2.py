# -*- coding: utf-8 -*-

import ser_c
import cmd_c
import sys
import os
import time

hostname = "www.google.com"  # example
check = 0

def ping_reboot():
    global check
    response = os.system("ping -c 1 " + hostname)
    print '--------------------- checking network ---------------------> ', check
    # and then check the response...
    if response == 0:
        print hostname, 'is up!'
        with open('./net_ok.txt', 'a') as f:
            f.write(time.ctime()+' -------- ok!\n')
        return check

    else:
        print hostname, 'is down!'
        with open('./net_down.txt', 'a') as f:
            f.write(time.ctime()+' -------- Down!\n')
        time.sleep(3)
        if check > 10:
            os.system("sudo reboot")
        return check+1

try :

    fc = os.system("ls connect_env.txt")
    usb_c = os.system("ls /dev/ttyUSB0")
    txt_workno = os.system("ls txt_workno.txt")
    if fc != 0 or usb_c != 0 or txt_workno != 0:
        raise MyError()
except :
    print "configuration is not supported"
    sys.exit() 

else :
    if fc == 0 and usb_c == 0 and txt_workno == 0:
        print "Reading from connection file\n"
        print "possible connecting"
        print "Reading from txt_workno\n"
        with open("connect_env.txt", 'r') as fr :
            buf_lines = fr.readlines()
        row_machine = buf_lines[4:5]
        row_sequence_time = buf_lines[7:8]
        row_tmp_id_num = buf_lines[8:9]
        tmp_id_num = int((row_tmp_id_num[0].replace('tmp_id_num = ', ''))[:-2])
        zone_id = []
        for i in range(0, tmp_id_num) :
            raw_id = buf_lines[(i+9):(i+10)]
            zone_id.append(int(raw_id[0][12:-2]))
        zone_id.append(int(buf_lines[(tmp_id_num+9):(tmp_id_num+10)][0][14:-2]))
        mchcd = (row_machine[0].replace('machine = ', ''))[:-2]
        sequence_t = float((row_sequence_time[0].replace('sequence_cycle = ', ''))[:-2])
        print 'id = ', zone_id        
        while True :

            check = ping_reboot()
            #for time check
            #start_time = time.time()
            
            #initial
            today = time.strftime("%y-%m-%d")
            today_log = today+'.txt'
            today_dir_path = time.strftime("%y-%b")
            tempdata = []
            send_to_db_data =[]
            c_parsing_data = []
            t_parsing_data = []
            origindir = os.getcwd()
            logdir = origindir + '/'+ today_dir_path
            
            #id / check current data
            for i in range(0, tmp_id_num+1) :
                time.sleep(sequence_t)
                if i == tmp_id_num:
                    pre_send_data = cmd_c.protocol(41, 's', zone_id[i], '')
                    print pre_send_data
                    r_data = ser_c.ser_f(pre_send_data)
                    if r_data == None :
                        c_parsing_data = [ '', '', '', '', '']
                    else :
                        c_parsing_data = cmd_c.protocol(41, 'r', zone_id[i], r_data)
                    print c_parsing_data
                    break
                else :
                    pre_send_data = cmd_c.protocol(31, 's', zone_id[i], '')
                    print pre_send_data
                    r_data = ser_c.ser_f(pre_send_data)
                    if r_data == None :
                        t_parsing_data = [ '', '', '', '', '', '', '', '', '', '', '', '']
                    else :
                        t_parsing_data = cmd_c.protocol(31, 'r', zone_id[i], r_data)
                    print t_parsing_data
                tempdata += t_parsing_data
            if len(tempdata) == 84 :
                send_to_db_data = c_parsing_data + [mchcd] + tempdata
            else :  
                moredata = 84 - len(tempdata)
                for i in range(len(tempdata), 84) :
                    tempdata.append('')
                send_to_db_data = c_parsing_data + [mchcd] + tempdata

            time.sleep(sequence_t)
            
            #send to db, current status
            db_cmd = 4 #usp_xngat11t_r_test
            db_data = cmd_c.db_check(db_cmd, tuple(send_to_db_data))
            print db_data
            '''
            if db_data == None :
                print 'data is not inserted in DB'
                with open(today_log, 'a') as log :
                    log_sentense = ctime() + '\n' + 'data is not inserted in DB'+'\n' + str(send_to_db_data) +'\n' + '--------------------------------' + '\n'
                    log.write(log_sentense)
            '''    
            time.sleep(sequence_t)
            
            #catch from text work number
            with open('txt_workno.txt', 'r') as fr :
                buf_lines = fr.readlines()
                before_work_no = buf_lines[-1:]
                wordno = str(before_work_no[0][:-1])
            
            #new work check
            db_cmd = 1 #usp_xnwrk_s
            db_data = cmd_c.db_check(db_cmd, '')
            print db_data
            if db_data == None :
                print 'db cmd = ', db_cmd
                print 'no data in db or no working start'
                os.chdir(logdir)
                with open(today_log, 'a') as log :
                    log_sentense = time.ctime() + '\n' + 'from DB, no working data' +'\n' + '--------------------------------' + '\n'
                    log.write(log_sentense)
                os.chdir(origindir)
            else :
                print 'data input start'
                print db_data
                planqty = str(format(db_data[0], '04X'))
                cavity = str(format(db_data[1], '02X'))
                prodqty = str(format(db_data[2], '04X'))
                wordno = str(db_data[3])
                with open('txt_workno.txt', 'a') as fa :
                    log_sentense = time.ctime() + '\n' + wordno + '\n'
                    fa.write(log_sentense)
                
                pre_send_data = cmd_c.protocol(44, 's', zone_id[tmp_id_num], '')
                r_data = ser_c.ser_f(pre_send_data)
                print r_data
                pre_send_data = cmd_c.protocol(42, 's', zone_id[tmp_id_num], planqty)
                r_data = ser_c.ser_f(pre_send_data)
                print r_data    
                pre_send_data = cmd_c.protocol(43, 's', zone_id[tmp_id_num], cavity)
                r_data = ser_c.ser_f(pre_send_data)
                print r_data
                pre_send_data = cmd_c.protocol(46, 's', zone_id[tmp_id_num], prodqty)
                r_data = ser_c.ser_f(pre_send_data)
                print r_data
                
                #check for work start
                pre_send_data = cmd_c.protocol(41, 's', zone_id[tmp_id_num], '')
                r_data = ser_c.ser_f(pre_send_data)
                
                if r_data == None :
                    print "can't input data"
                    pass
                else :
                    c_parsing_data = cmd_c.protocol(41, 'r', zone_id[tmp_id_num], r_data)                  
                    if c_parsing_data[0] == db_data[0] and c_parsing_data[1] == db_data[2] and c_parsing_data[4] == db_data[1] :
                        #usp_xnwrk_u / mchcd
                        db_cmd = 5 #usp_xnwrk_u
                        db_data = cmd_c.db_check(db_cmd, '')
                        print db_data
                    else :
                        print "can't input data"
                        pass
                
            time.sleep(sequence_t)
                
            db_cmd = 2 #usp_xnbad_s
            db_data = cmd_c.db_check(db_cmd, wordno)
            print db_data
            if db_data == None :
                print 'db cmd = ', db_cmd
                print 'no data in db or no working start'
                os.chdir(logdir)
                with open(today_log, 'a') as log :
                    log_sentense = time.ctime() + '\n' + 'from DB, no badqty data' +'\n' + '--------------------------------' + '\n'
                    log.write(log_sentense)
                os.chdir(origindir)
            else :
                print db_data
                badqty = str(format(int(db_data[0]), '04X'))
                pre_send_data = cmd_c.protocol(45, 's', zone_id[tmp_id_num], badqty)
                r_data = ser_c.ser_f(pre_send_data)
                if r_data == None :
                    print 'badqty is not inserted in FP'
                    os.chdir(logdir)
                    with open(today_log, 'a') as log :
                        log_sentense = time.ctime() + '\n' + 'data is not inserted in DB'+'\n' + str(badqty) +'\n' + '--------------------------------' + '\n'
                        log.write(log_sentense)
                    os.chdir(origindir) 
            
            time.sleep(sequence_t)
            
            db_cmd = 3 #usp_tmset01t_s01
            db_data = cmd_c.db_check(db_cmd, '')
            print db_data
            if db_data == None :
                print 'db cmd = ', db_cmd
                print 'no data in db or no working start'
                os.chdir(logdir)
                with open(today_log, 'a') as log :
                    log_sentense = time.ctime() + '\n' + 'from DB, no temp set data' +'\n' + '--------------------------------' + '\n'
                    log.write(log_sentense)
                os.chdir(origindir) 
                
            else :
                temp_data = cmd_c.temp_parsing(db_data)

                for i in range(0, tmp_id_num) :
                    for j in range(1, 3) :
                        for k in range(0, 3) :
                            if k == 0 :
                                sen_no = str('{:02x}'.format(int(j)))
                                data = sen_no + temp_data[i][j-1][k]
                                pre_send_data = cmd_c.protocol(32, 's', zone_id[i], data)
                                print pre_send_data
                                r_data = ser_c.ser_f(pre_send_data)
                                print r_data
                            elif k == 1 :
                                sen_no = str('{:02x}'.format(int(j)))
                                data = sen_no + temp_data[i][j-1][k]
                                pre_send_data = cmd_c.protocol(33, 's', zone_id[i], data)
                                print pre_send_data
                                r_data = ser_c.ser_f(pre_send_data)
                                print r_data
                            elif k == 2 :
                                sen_no = str('{:02x}'.format(int(j)))
                                data = sen_no + temp_data[i][j-1][k]
                                pre_send_data = cmd_c.protocol(34, 's', zone_id[i], data)
                                print pre_send_data
                                r_data = ser_c.ser_f(pre_send_data)
                                print r_data

                db_cmd = 6 #usp_tmset01t_u02
                db_data = cmd_c.db_check(db_cmd, '')
                print db_data

            #for time check
            '''
            time.sleep(sequence_t)
            end_time = time.time() - start_time
            with open('timecheck.txt', 'a') as log :
                    log_sentense = str(end_time) + '\n'
                    log.write(log_sentense)
            '''
