from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
import pymssql
import time
import os

hostname = "192.168.30.1"  # example
check = 0

def ping_reboot():
    global check
    response = os.system("ping -c 1 " + hostname)
    print '--------------------- checking network ---------------------> ', check
    # and then check the response...
    if response == 0:
        print hostname, 'is up!'
        return check

    else:
        print hostname, 'is down!'
        time.sleep(3)
        if check > 10:
            os.system("sudo reboot")
        return check+1

def read_holding_register_int64(i):
    time.sleep(0.01)
    global b
    print b[i]
    d = None
    d = int(b[i])
    rr = client.read_holding_registers(d, 8)
    assert (rr.function_code < 0x80)
    print rr
    print rr.registers
    decoder = BinaryPayloadDecoder.fromRegisters(list(rr.registers), Endian.Big, wordorder=Endian.Little)
    print 'decoder = ' + str(decoder)
    frr = str("{0:.2f}".format(float(decoder.decode_64bit_int()) / 1000000))
    print 'frr = ' + frr
    reg_data.append(frr)

def read_holding_register_int32(i):
    time.sleep(0.01)
    global b
    print b[i]
    d = None
    d = int(b[i])
    rr = client.read_holding_registers(d, 4)
    assert (rr.function_code < 0x80)
    print rr
    print rr.registers
    decoder = BinaryPayloadDecoder.fromRegisters(list(rr.registers), Endian.Big, wordorder=Endian.Little)
    print 'decoder = ' + str(decoder)
    frr = str(decoder.decode_32bit_int())
    print 'frr = ' + frr
    reg_data.append(frr)

def read_holding_register_uint32(i):
    time.sleep(0.01)
    global b
    print b[i]
    d = None
    d = int(b[i])
    rr = client.read_holding_registers(d, 4)
    assert (rr.function_code < 0x80)
    print rr
    print rr.registers
    decoder = BinaryPayloadDecoder.fromRegisters(list(rr.registers), Endian.Big, wordorder=Endian.Little)
    print 'decoder = ' + str(decoder)
    frr = str(decoder.decode_32bit_uint())
    print 'frr = ' + frr
    reg_data.append(frr)

def read_holding_register_float32(i):
    time.sleep(0.01)
    global b
    print b[i]
    d = None
    d = int(b[i])
    rr = client.read_holding_registers(d, 4)
    assert (rr.function_code < 0x80)
    print rr
    print rr.registers
    decoder = BinaryPayloadDecoder.fromRegisters(list(rr.registers), Endian.Big, wordorder=Endian.Little)
    print 'decoder = ' + str(decoder)
    frr = str("{0:.2f}".format(decoder.decode_32bit_float()))
    print 'frr = ' + frr
    reg_data.append(frr)

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
    
    host = '192.168.30.150'
    port = '502'
    client = ModbusTcpClient(host, port)

    host2 = '192.168.30.177'
    client2 = ModbusTcpClient(host2, port)

    while True :

        check = ping_reboot()

        ##LS-001
        #host = '192.168.30.150'
        #port = '502'
        #client = ModbusTcpClient(host, port)
        client.connect()
        reg_data = []
        print 'client connection-------------------- ', client.connect()
        for i in range(0, a):

            if i == 2 or 3 or 17 or 26:
                read_holding_register_int64(i)

            elif i == 1 or 27 or 28 or 29 or 30:
                read_holding_register_int32(i)

            elif i == 31:
                read_holding_register_uint32(i)

            else:
                read_holding_register_float32(i)


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
        client.close()

        ##LS-002
        #host2 = '192.168.30.177'
        #port = '502'
        mchcd2 = '2053'
        #client2 = ModbusTcpClient(host2, port)
        client2.connect()
        reg_data = []
        for i in range(0, a):

            if i == 2 or 3 or 17 or 26:
                read_holding_register_int64(i)

            elif i == 1 or 27 or 28 or 29 or 30:
                read_holding_register_int32(i)

            elif i == 31:
                read_holding_register_uint32(i)

            else:
                read_holding_register_float32(i)
            # reg_data.append(rr2.registers[0])
        reg_data.insert(0, mchcd2)
        print reg_data
        prod_data = tuple(reg_data)
        print prod_data
        time.sleep(5)
        conn = pymssql.connect(server[:-2], user[:-2], password[:-2], database[:-2], timeout=3)
        cursor = conn.cursor()
        cursor.callproc('usp_toSambaDBt', prod_data)

        time.sleep(0.01)
        conn.commit()
        conn.close()
        client2.close()
    
except ValueError:
    print("Error")
