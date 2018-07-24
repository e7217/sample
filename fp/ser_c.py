import serial
import os
import time
import shutil

def ser_f (data) :
    
    try :
        port = '/dev/ttyUSB0'
        sys_file = 'connect_env.txt'
        fc = os.system("ls %s" % sys_file)
        usb_c=os.system("ls %s" % port )
        
        #for log
        today = time.strftime("%y-%m-%d")
        today_dir_path = time.strftime("%y-%b")
        
        today_log = today+'.txt'
        
        #log delete
        a= time.time()
        b= a - 60*60*24*90
        del_day = time.gmtime(b)
        del_day_dir_path = time.strftime("%y-%b", del_day)
        #log logic / dir
        origindir = os.getcwd()
        logdir = origindir + '/'+ today_dir_path
        
        try :
            if not os.path.exists(today_dir_path):
                os.makedirs(today_dir_path)
                print 'making ' + today_dir_path
            else : 
                print 'be made ' + today_dir_path
            
            if os.path.exists(del_day_dir_path):
                shutil.rmtree(del_day_dir_path, ignore_errors=True)
                print 'removing ' + del_day_dir_path
            else :
                print 'no exist ' + del_day_dir_path
        except :
            pass
        
       
        if usb_c==0 and fc == 0 :
            print "possible connecting"
            ser = serial.Serial(port, 19200, timeout=0)
            ser.close()
            with open(sys_file, 'r') as fr :
                buf_lines = fr.readlines()
                row_send_cycle = buf_lines[5:6]
                row_response_count = buf_lines[6:7]
                send_cycle = float(row_send_cycle[0].replace('send_cycle = ', ''))
                response_count = int(row_response_count[0].replace('response_count = ', ''))
            
            hex_data = data.decode("hex")
            ser.open()
            ser.write(hex_data)
            
            os.chdir(logdir)
            with open(today_log, 'a') as log :
                log_sentense = time.ctime() + '\n' + data + '\n' + 'send to FP' +'\n' + '--------------------------------' + '\n'
                log.write(log_sentense)
            os.chdir(origindir)   
            
            i = 0

            while 1 :
                time.sleep(send_cycle)
                r_data = ser.read(100) 
                ser.close()
                if r_data != None :
                    a = r_data.encode("hex")
                    print a
                    if a[-2:] == '03' and a[:2] == '02' :
                        # temp or cnt need more checking
                        if len(a) == 56 and data[4:6] == '31':
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'parsed' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir) 
                            return a
                        elif len(a) == 16 and data[4:6] == '32':
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'setting' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a
                        elif len(a) == 16 and data[4:6] == '33':
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'set high_L' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a
                        elif len(a) == 16 and data[4:6] == '34':
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'set low_L' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a
                        elif len(a) == 16 and data[4:6] == '35':
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'offset' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a
                        elif len(a) == 46 and data[4:6] == '41':
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'parsed' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a
                        elif len(a) == 16 and data[4:6] == '42' :
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'plan qty' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a
                        elif len(a) == 16 and data[4:6] == '43' :
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'cavity' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a
                        elif len(a) == 16 and data[4:6] == '44' :
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'reset' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a
                        elif len(a) == 16 and data[4:6] == '45' :
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'bad qty' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a                            
                        elif len(a) == 16 and data[4:6] == '46' :
                            os.chdir(logdir)
                            with open(today_log, 'a') as log :
                                log_sentense = time.ctime() + '\n' + a + '\n' + 'prod qty' +'\n' + '--------------------------------' + '\n'
                                log.write(log_sentense)
                            os.chdir(origindir)
                            return a 
                        else :
                            continue
                    elif i != response_count:

                        print 'no received from FP'
                        i += 1
                        ser.open()
                        ser.write(hex_data)
                    
                    elif i == response_count :
                        os.chdir(logdir)
                        with open(today_log, 'a') as log :
                            log_sentense = time.ctime() + '\n' + 'no data coming' + '\n' + '--------------------------------' + '\n'
                            log.write(log_sentense)
                        os.chdir(origindir)
                        ser.close()
                        break
            

        elif usb_c !=0 :  
            print "impossible connecting"       
            
        elif fc != 0:
            print "configuration is not supported" 

    except :
        pass