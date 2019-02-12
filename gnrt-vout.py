#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time
import serial
import modbus_tk.defines as tkCst
import modbus_tk.modbus_rtu as tkRtu
import os.path

log = '/var/log/or_gnrt_rs485'

if os.path.exists('/dev/ttyVS0') is True:
	time.sleep(59)

cnt = 5
try:
	prc = subprocess.Popen(['screen','-dmS','socat_tmp', 'socat','-d','-d','pty,link=/dev/ttyVS0,raw','tcp:10.101.254.250:50'],stdout=subprocess.PIPE)
except Exeption:
	print('Fail')
time.sleep(15)
mb_rtu = tkRtu.RtuMaster(serial.Serial('/dev/ttyVS0', baudrate=9600, bytesize=8, parity='N',stopbits=1))

mb_rtu.open
mb_rtu.set_timeout(3)
mb_rtu.set_verbose(True)

for i in range (cnt):
	fin_str = ' '
	print 'READ_HOLDING_REGISTERS >>> Sample: ' + str(i)
	get_reg = mb_rtu.execute(1, tkCst.READ_HOLDING_REGISTERS, 1, 100)
	for j in range (len(get_reg)):
		fin_str += str(get_reg[j]) + ' '
	print fin_str
	time.sleep(1)
	fin_str += '\n' + str(time.strftime('%d-%m-%Y %H:%M:%S')) + ' Vout1 = ' + str(get_reg[6]) + ' Vout2 = ' + str(get_reg[7]) + ' Vout3 = ' + str(get_reg[8]) + '\n'
prc.terminate()

log_file = open(log, 'a')
log_file.write(fin_str)
log_file.close()
