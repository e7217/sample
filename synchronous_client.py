from pymodbus.client.sync import ModbusTcpClient
import pymssql
import time

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
try:
    conn = pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout = 3)
    cursor = conn.cursor()
    cursor.execute('usp_modset01t_s01 %s' % proc_mchcd)
    time.sleep(0.01)
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    time.sleep(0.01)
    row_list = list(row)
    address_list = row_list[3:]
    print address_list
    a = address_list.index(None)
    b = address_list[0:a]
    reg_no = []
    
    host = '192.168.20.2'
    port = '502'
    client = ModbusTcpClient(host, port)
    client.connect()
    while True :
        reg_data = []
        for i in range(0, a):
            time.sleep(0.01)
            print b[i]
            d = int(b[i])
            rr = client.read_holding_registers(d,1, unit = 1)
            assert(rr.function_code < 0x80)
            print rr
            print rr.registers
            reg_data.append(rr.registers[0])
        reg_data.insert(0, mchcd)
        print reg_data
        prod_data = tuple(reg_data)
        print prod_data
        time.sleep(5)
        conn = pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout = 3)
        cursor = conn.cursor()
        cursor.callproc('usp_toSambaDBt', prod_data)
        
        time.sleep(0.01)
        conn.commit()
        conn.close()
    
except ValueError:
    print("Error")
