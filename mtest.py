from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import pymssql
import time
import os

hostname = "192.168.30.1"  # example
check = 0

a=1
b=2

try:
    reg_no = []
    
    host = '192.168.30.150'
    port = '502'
    client = ModbusTcpClient(host, port)

    host2 = '192.168.30.177'
    client2 = ModbusTcpClient(host2, port)

    while True :

        ##LS-001
        #host = '192.168.30.150'
        #port = '502'
        #client = ModbusTcpClient(host, port)
        client.connect()
        reg_data = []
        print 'client connection-------------------- ', client.connect()

        r1 = client.read_holding_registers(a,b)
        print 'r1 = ' + r1.registers
        decoder = BinaryPayloadDecoder.fromRegisters(r1.registers, Endian.Big, wordorder=Endian.Little)
        print 'decoder = ' + str(decoder)
        print 'fr1 = ' + str(decoder.decode_32bit_float())
        reg_data.append(str(decoder.decode_32bit_float()))
        print reg_data

    
except ValueError:
    print("Error")
