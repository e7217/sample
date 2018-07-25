# -*- coding: utf-8 -*-

import time
import pymssql
import os
import shutil

def protocol (cmd, mode, zone_id, data):
    if cmd == 31 : 
        if mode == 's' : 
            print ('Check Tmp, id = %s' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            str_data = '00000000'
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + str_data + etx
            return s_data
            
        elif  mode == 'r' :
            print ('received data will be parsing, ID = %s' % (zone_id))
            #rec_stx = data[0:2]
            #rec_id = data[2:4] 
            #rec_cmd = data[4:6]
            #rec_dspno = data[6:8]
            rec_1_error = data[8:10]
            rec_1_now_tp = data[10:14]
            rec_1_set_tp = data[14:18]
            rec_1_set_high_tp = data[18:22]
            rec_1_set_low_tp = data[22:26]
            rec_1_offset = data[26:28]
            #rec_1_sign = data[28:30]
            rec_2_error = data[30:32]
            rec_2_now_tp = data[32:36]
            rec_2_set_tp = data[36:40]
            rec_2_set_high_tp = data[40:44]
            rec_2_set_low_tp = data[44:48]
            rec_2_offset = data[48:50]
            #rec_2_sign = data[50:52]
            #rec_bcc = data[52:54]
            #rec_etx = data[54:] 
            #rec_1_sl= (int(rec_1_set_high_tp, 16) -  int(rec_1_set_low_tp, 16))/2
            #rec_2_sl= (int(rec_2_set_high_tp, 16) -  int(rec_2_set_low_tp, 16))/2
            p_data = [int(rec_1_error, 16), int(rec_1_now_tp, 16), int(rec_1_set_tp, 16), int(rec_1_set_high_tp, 16), int(rec_1_set_low_tp, 16),int(rec_1_offset, 16), int(rec_2_error, 16), int(rec_2_now_tp, 16), int(rec_2_set_tp, 16), int(rec_2_set_high_tp, 16), int(rec_2_set_low_tp, 16),int(rec_2_offset, 16)]

            print 'parsing complete 31:', time.ctime()
            return p_data    
            
    elif cmd == 32 : 
        if mode == 's' : 
            print ('set temp, ID = %s' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            bcc = '00'
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data + bcc + etx
            return s_data
    
    elif cmd == 33 :         
        if mode == 's' : 
            print ('set high_Limit, ID = %s' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            bcc = '00'
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data + bcc + etx
            return s_data
    
    elif cmd == 34 :         
        if mode == 's' : 
            print ('set low_Limit, ID = %s' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            bcc = '00'
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data + bcc + etx
            return s_data
        
    elif cmd == 35 :         
        if mode == 's' : 
            print ('offset, ID = %s' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            bcc = '00'
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data + bcc + etx
            return s_data
    
            
    elif cmd == 41 :
        if mode == 's' : 
            print ('Check cnt, ID = %s ' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            data_41 = '00000000'
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data_41 +  etx
            return s_data
        
        elif  mode == 'r' :
            print ('received data will be parsing, ID = %s' % (zone_id))
            #rec_stx = data[0:2]
            #rec_id = data[2:4]
            #rec_cmd = data[4:6]
            rec_planqty = data[6:10]
            rec_cavity = data[10:12]
            rec_prodqty = data[12:16]
            rec_badqty = data[16:20]
            rec_goodqty = data[20:24]
            #rec_hopaim_a = data[24:26]
            #rec_hopaim_b = data[26:28]
            #rec_level = data[28:30]
            #rec_reserved = data[30:42]
            #rec_bcc = data[42:44]
            #rec_etx = data[44:]
                                    
            r_data = [int(rec_planqty, 16), int(rec_prodqty, 16), int(rec_badqty, 16), int(rec_goodqty, 16), int(rec_cavity, 16)]
            print 'parsing complete 41:', time.ctime()
            return r_data
            
    elif cmd == 42 :
        if mode == 's' : 
            print ('Setting planqty, ID = %s ' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            bcc = '0000'
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data + bcc + etx
            return s_data           
            
    elif cmd == 43 :
        if mode == 's' : 
            print ('Setting cavity, ID = %s ' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            bcc = '000000'            
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data + bcc + etx
            return s_data

    elif cmd == 44 :
        if mode == 's' : 
            print ('reset cnt FP, ID = %s ' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            data_44 = '00000000'
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data_44 + etx
            return s_data

    elif cmd == 45 :
        if mode == 's' : 
            print ('Setting badqty, ID = %s ' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            bcc = '0000'           
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd +data + bcc + etx
            return s_data

    elif cmd == 46 :
        if mode == 's' : 
            print ('Setting prodqty, ID = %s ' % (zone_id))
            stx = "02"
            str_id = str('{:02x}'.format(int(zone_id)))
            str_cmd = str(cmd)
            bcc = '0000'            
            etx = "03" #etx   
            s_data = stx + str_id + str_cmd + data + bcc + etx
            return s_data

def db_check (cmd, data):            
    sqldata_1 =[]
    sqldata_2 =[]
    col_names_1 = ('goalqty', 'cavity', 'prodqty', 'wordno')
    col_names_2 = ('mchcd','temp_set01','temp_sl01'\
    ,'temp_set02','temp_sl02','temp_set03','temp_sl03'\
    ,'temp_set04','temp_sl04','temp_set05','temp_sl05'\
    ,'temp_set06','temp_sl06','temp_set07','temp_sl07'\
    ,'temp_set08','temp_sl08','temp_set09','temp_sl09'\
    ,'temp_set10','temp_sl10','temp_set11','temp_sl11'\
    ,'temp_set12','temp_sl12','temp_set13','temp_sl13'\
    ,'temp_set14','temp_sl14')
    with open("connect_env.txt", 'r') as fr :
        buf_lines = fr.readlines()
        row_server = buf_lines[0:1]
        row_user = buf_lines[1:2]
        row_password = buf_lines[2:3]
        row_database = buf_lines[3:4]
        row_machine = buf_lines[4:5]
        server = row_server[0].replace('server = ', '')
        user = row_user[0].replace('user = ', '')
        password = row_password[0].replace('password = ', '')
        database = row_database[0].replace('database = ', '')
        mchcd = (row_machine[0].replace('machine = ', ''))[:-2]
    proc_mchcd = str("'%s'" % mchcd) 
    proc_value_1 = ("'N'", "%s" % proc_mchcd)
    today = time.strftime("%y-%m-%d")
    today_dir_path = time.strftime("%y-%b")
    today_log = today +'db.txt'
    
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
    
    #for working start
    if cmd == 1 : 
        try :
            with pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout = 3) as conn:
                time.sleep(0.01)
                print 'db_step_1 connection'
                with conn.cursor() as cursor:
                    time.sleep(0.01)
                    print 'db_step_2 cursor'
                    cursor.execute(('execute usp_xnwrk_s %s, %s;') % proc_value_1 )
                    time.sleep(0.01)
                    print 'db_step_3 query'
                    try:
                        results = cursor.fetchone()
                        time.sleep(0.01)
                        print results
                        print 'db_step_4 completed'
                        for i in range(len(col_names_1)) :
                            for j in range(len(cursor.description)) :
                                desc = cursor.description[j]
                                if col_names_1[i] == str(desc[0]):
                                    column_no_1 = j
                                    break
                            sqldata_1.append(results[column_no_1])
                        print sqldata_1
                        print 'db_step5'
                    except : 
                        print 'passed'
                        pass

            os.chdir(logdir)
            with open(today_log, 'a') as log :
                log_sentense = time.ctime() + '\n' + str(sqldata_1[0]) + ', ' + str(sqldata_1[1]) + ', ' + str(sqldata_1[2]) + ', ' + str(sqldata_1[3]) + '\n' + 'from usp_xnwrk_s' +'\n' + '--------------------------------' + '\n'
                log.write(log_sentense) 
            os.chdir(origindir)  
            return sqldata_1
        except :
            print 'no data in db'
            pass
        
    #for bad find   
    elif cmd == 2 :
        proc_data = str("'%s'" % data)
        proc_value_2 = (proc_mchcd, proc_data)
        print proc_data
        try :
            with pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout = 3) as conn:
                time.sleep(0.01)
                print 'db_step_1'
                with conn.cursor() as cursor:
                    time.sleep(0.01)
                    print 'db_step_2'
                    cursor.execute(('usp_xnbad_s %s, %s;') % proc_value_2)
                    time.sleep(0.01)
                    print 'db_step_3'
                    try:
                        results = cursor.fetchone()
                        time.sleep(0.01)
                        print results
                        print 'db_step_4 completed'
                    except : 
                        print 'passed'
                        pass
            os.chdir(logdir)
            with open(today_log, 'a') as log :
                log_sentense = time.ctime() + '\n' + str(results[0]) + '\n' + 'bad cnt from usp_xnbad_s' +'\n' + '--------------------------------' + '\n'
                log.write(log_sentense)    
            os.chdir(origindir)
            return results
        
        except :
            print 'no data in db'
            pass

 
#if for tmp setting   
    elif cmd == 3 :
        try :
            with pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout = 3) as conn:
                time.sleep(0.01)
                print 'db_step_1'
                with conn.cursor() as cursor:
                    time.sleep(0.01)
                    print 'db_step_2'
                    cursor.execute(('execute usp_tmset01t_s01 %s, %s;') % proc_value_1)
                    time.sleep(0.01)
                    print 'db_step_3'
                    try :
                        results = cursor.fetchone()
                        time.sleep(0.01)
                        print results
                        print 'db_step_4 completed'
                        for i in range(len(col_names_2)) :
                            for j in range(len(cursor.description)) :
                                desc = cursor.description[j]
                                if col_names_2[i] == str(desc[0]):
                                    column_no_2 = j
                                    break
                            sqldata_2.append(results[column_no_2])
                    except : 
                        print 'passed'
                        pass
            os.chdir(logdir)
            print sqldata_2
            with open(today_log, 'a') as log :
                log_sentense = time.ctime() + '\n' + str(sqldata_2[0]) \
                                        + ', ' + str(sqldata_2[1]) \
                                        + ', ' + str(sqldata_2[2]) \
                                        + ', ' + str(sqldata_2[3]) \
                                        + ', ' + str(sqldata_2[4]) \
                                        + ', ' + str(sqldata_2[5]) \
                                        + ', ' + str(sqldata_2[6]) \
                                        + ', ' + str(sqldata_2[7]) \
                                        + ', ' + str(sqldata_2[8]) \
                                        + ', ' + str(sqldata_2[9]) \
                                        + ', ' + str(sqldata_2[10]) \
                                        + ', ' + str(sqldata_2[11]) \
                                        + ', ' + str(sqldata_2[12]) \
                                        + ', ' + str(sqldata_2[13]) \
                                        + ', ' + str(sqldata_2[14]) \
                                        + ', ' + str(sqldata_2[15]) \
                                        + ', ' + str(sqldata_2[16]) \
                                        + ', ' + str(sqldata_2[17]) \
                                        + ', ' + str(sqldata_2[18]) \
                                        + ', ' + str(sqldata_2[19]) \
                                        + ', ' + str(sqldata_2[20]) \
                                        + ', ' + str(sqldata_2[21]) \
                                        + ', ' + str(sqldata_2[22]) \
                                        + ', ' + str(sqldata_2[23]) \
                                        + ', ' + str(sqldata_2[24]) \
                                        + ', ' + str(sqldata_2[25]) \
                                        + ', ' + str(sqldata_2[26]) \
                                        + ', ' + str(sqldata_2[27]) \
                                        + ', ' + str(sqldata_2[28]) \
                                        + '\n' + 'from usp_tmset01t_s01' +'\n' + '--------------------------------' + '\n'
                log.write(log_sentense) 
            os.chdir(origindir) 
            return sqldata_2
        
        except :
            print 'no data in db'
            pass

#if for tmp data input
    elif cmd == 4 :
        try :
            conn = pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout = 3)
            time.sleep(0.01)
            print 'db_step_1'
            cursor = conn.cursor()
            time.sleep(0.01)
            print 'db_step_2'
            cursor.callproc('usp_xngat11t_r_test', data)
            time.sleep(0.01)
            print 'db_step_3'
            conn.commit()
            time.sleep(0.01)
            print 'db_step_4'
            conn.close()
            time.sleep(0.01)
            print 'db_step_5 connection closed'
        except :
            print 'data is not input in db'

#if for work start update
    elif cmd == 5 :
        try :
            conn = pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout = 3)
            time.sleep(0.01)
            print 'db_step_1'
            cursor = conn.cursor()
            time.sleep(0.01)
            print 'db_step_2'
            cursor.callproc('usp_xnwrk_u', [mchcd])
            time.sleep(0.01)
            print 'db_step_3-1'
            # 180529 추가내용.
            cursor.callproc('usp_xngat11t_i02', [None, mchcd, 'S', 0])
            time.sleep(0.01)
            print 'db_step_3-2'
            conn.commit()
            time.sleep(0.01)
            print 'db_step_4'
            conn.close()
            time.sleep(0.01)
            print 'db_step_5 connection closed'
            
        except :
            print 'data is not input in db'

#if for 
    elif cmd == 6 :
        try :
            conn = pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout = 3)
            time.sleep(0.01)
            print 'db_step_1'
            cursor = conn.cursor()
            time.sleep(0.01)
            print 'db_step_2'
            cursor.callproc('usp_tmset01t_u02', [mchcd])
            time.sleep(0.01)
            print 'db_step_3'
            conn.commit()
            time.sleep(0.01)
            print 'db_step_4'
            conn.close()
            time.sleep(0.01)
            print 'db_step_5 connection closed'
            
        except :
            print 'data is not input in db'

            
def temp_parsing (db_data):
    temp_set01 = db_data[1]
    temp_sl01= db_data[2]
    temp_high_L_01 = temp_sl01
    if temp_set01 <=  temp_sl01 :
        temp_low_L_01 = 0 
    else :
        temp_low_L_01 = temp_sl01
    
    temp_set02= db_data[3]
    temp_sl02= db_data[4]
    temp_high_L_02 = temp_sl02
    if temp_set02 <=  temp_sl02 :
        temp_low_L_02 = 0 
    else :
        temp_low_L_02 = temp_sl02
   
    temp_set03= db_data[5]
    temp_sl03= db_data[6]
    temp_high_L_03 = temp_sl03
    if temp_set03 <=  temp_sl03 :
        temp_low_L_03 = 0 
    else :
        temp_low_L_03 = temp_sl03
    
    temp_set04= db_data[7]
    temp_sl04= db_data[8]
    temp_high_L_04 = temp_sl04
    if temp_set04 <=  temp_sl04 :
        temp_low_L_04 = 0 
    else :
        temp_low_L_04 = temp_sl04
    
    temp_set05= db_data[9]
    temp_sl05= db_data[10]
    temp_high_L_05 = temp_sl05
    if temp_set05 <=  temp_sl05 :
        temp_low_L_05 = 0 
    else :
        temp_low_L_05 = temp_sl05
    
    temp_set06= db_data[11]
    temp_sl06= db_data[12]
    temp_high_L_06 = temp_sl06
    if temp_set06 <=  temp_sl06 :
        temp_low_L_06 = 0 
    else :
        temp_low_L_06 = temp_sl06
    
    temp_set07= db_data[13]
    temp_sl07= db_data[14]
    temp_high_L_07 = temp_sl07
    if temp_set07 <=  temp_sl07 :
        temp_low_L_07 = 0 
    else :
        temp_low_L_07 = temp_sl07
    
    temp_set08= db_data[15]
    temp_sl08= db_data[16]
    temp_high_L_08 = temp_sl08
    if temp_set08 <=  temp_sl08 :
        temp_low_L_08 = 0 
    else :
        temp_low_L_08 = temp_sl08
    
    temp_set09= db_data[17]
    temp_sl09= db_data[18]
    temp_high_L_09 = temp_sl09
    if temp_set09 <=  temp_sl09 :
        temp_low_L_09 = 0 
    else :
        temp_low_L_09 = temp_sl09
    
    temp_set10= db_data[19]
    temp_sl10= db_data[20]
    temp_high_L_10 = temp_sl10
    if temp_set10 <=  temp_sl10 :
        temp_low_L_10 = 0 
    else :
        temp_low_L_10 = temp_sl10
        
    temp_set11= db_data[21]
    temp_sl11= db_data[22]
    temp_high_L_11 = temp_sl11
    if temp_set11 <=  temp_sl11 :
        temp_low_L_11 = 0 
    else :
        temp_low_L_11 = temp_sl11
    
    temp_set12= db_data[23]
    temp_sl12= db_data[24]
    temp_high_L_12 = temp_sl12
    if temp_set12 <=  temp_sl12 :
        temp_low_L_12 = 0 
    else :
        temp_low_L_12 = temp_sl12
     
    temp_set13= db_data[25]
    temp_sl13= db_data[26]
    temp_high_L_13 = temp_sl13
    if temp_set13 <=  temp_sl13 :
        temp_low_L_13 = 0 
    else :
        temp_low_L_13 = temp_sl13   
    
    temp_set14= db_data[27]
    temp_sl14= db_data[28]
    temp_high_L_14 = temp_sl14
    if temp_set14 <=  temp_sl14 :
        temp_low_L_14 = 0 
    else :
        temp_low_L_14 = temp_sl14
        
    temp_zone_1 = []
    temp_zone_2 = []
    temp_zone_3 = []
    temp_zone_4 = []
    temp_zone_5 = []
    temp_zone_6 = []
    temp_zone_7 = []
    temp_zone_8 = []
    temp_zone_9 = []
    temp_zone_10 = []
    temp_zone_11 = []
    temp_zone_12 = []
    temp_zone_13 = []
    temp_zone_14 = []
    
    
    temp_zone_1.append(str(format(int(temp_set01), '04X')))
    temp_zone_1.append(str(format(int(temp_high_L_01), '04X')))
    temp_zone_1.append(str(format(int(temp_low_L_01), '04X')))
    
    temp_zone_2.append(str(format(int(temp_set02), '04X')))
    temp_zone_2.append(str(format(int(temp_high_L_02), '04X')))
    temp_zone_2.append(str(format(int(temp_low_L_02), '04X')))
    
    
    temp_zone_3.append(str(format(int(temp_set03), '04X')))
    temp_zone_3.append(str(format(int(temp_high_L_03), '04X')))
    temp_zone_3.append(str(format(int(temp_low_L_03), '04X')))
    
    temp_zone_4.append(str(format(int(temp_set04), '04X')))
    temp_zone_4.append(str(format(int(temp_high_L_04), '04X')))
    temp_zone_4.append(str(format(int(temp_low_L_04), '04X')))
    
    temp_zone_5.append(str(format(int(temp_set05), '04X')))
    temp_zone_5.append(str(format(int(temp_high_L_05), '04X')))
    temp_zone_5.append(str(format(int(temp_low_L_05), '04X')))
    
    temp_zone_6.append(str(format(int(temp_set06), '04X')))
    temp_zone_6.append(str(format(int(temp_high_L_06), '04X')))
    temp_zone_6.append(str(format(int(temp_low_L_06), '04X')))
    
    temp_zone_7.append(str(format(int(temp_set07), '04X')))
    temp_zone_7.append(str(format(int(temp_high_L_07), '04X')))
    temp_zone_7.append(str(format(int(temp_low_L_07), '04X')))
    
    temp_zone_8.append(str(format(int(temp_set08), '04X')))
    temp_zone_8.append(str(format(int(temp_high_L_08), '04X')))
    temp_zone_8.append(str(format(int(temp_low_L_08), '04X')))
    
    temp_zone_9.append(str(format(int(temp_set09), '04X')))
    temp_zone_9.append(str(format(int(temp_high_L_09), '04X')))
    temp_zone_9.append(str(format(int(temp_low_L_09), '04X')))
    
    temp_zone_10.append(str(format(int(temp_set10), '04X')))
    temp_zone_10.append(str(format(int(temp_high_L_10), '04X')))
    temp_zone_10.append(str(format(int(temp_low_L_10), '04X')))
    
    temp_zone_11.append(str(format(int(temp_set11), '04X')))
    temp_zone_11.append(str(format(int(temp_high_L_11), '04X')))
    temp_zone_11.append(str(format(int(temp_low_L_11), '04X')))
    
    temp_zone_12.append(str(format(int(temp_set12), '04X')))
    temp_zone_12.append(str(format(int(temp_high_L_12), '04X')))
    temp_zone_12.append(str(format(int(temp_low_L_12), '04X')))
    
    temp_zone_13.append(str(format(int(temp_set13), '04X')))
    temp_zone_13.append(str(format(int(temp_high_L_13), '04X')))
    temp_zone_13.append(str(format(int(temp_low_L_13), '04X')))
    
    temp_zone_14.append(str(format(int(temp_set14), '04X')))
    temp_zone_14.append(str(format(int(temp_high_L_14), '04X')))
    temp_zone_14.append(str(format(int(temp_low_L_14), '04X')))
    
    temp_data = []
    
    temp_id_1 = []
    temp_id_2 = []
    temp_id_3 = []
    temp_id_4 = []
    temp_id_5 = []
    temp_id_6 = []
    temp_id_7 = []

    temp_id_1.append(temp_zone_1)
    temp_id_1.append(temp_zone_2)
    temp_id_2.append(temp_zone_3)
    temp_id_2.append(temp_zone_4)
    temp_id_3.append(temp_zone_5)
    temp_id_3.append(temp_zone_6)
    temp_id_4.append(temp_zone_7)
    temp_id_4.append(temp_zone_8)
    temp_id_5.append(temp_zone_9)
    temp_id_5.append(temp_zone_10)
    temp_id_6.append(temp_zone_11)
    temp_id_6.append(temp_zone_12)
    temp_id_7.append(temp_zone_13)
    temp_id_7.append(temp_zone_14)
    
    temp_data.append(temp_id_1)
    temp_data.append(temp_id_2)
    temp_data.append(temp_id_3)
    temp_data.append(temp_id_4)
    temp_data.append(temp_id_5)
    temp_data.append(temp_id_6)
    temp_data.append(temp_id_7)
    
    return temp_data