#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import telnetlib
import re

if len(sys.argv) == 2:
        ip_sw = sys.argv[1]
else:
        print "The amount of attrib isn't correct."

def sw_acc(ip):
	rgx_nm = re.compile('([A-Za-z0-9-.]+)[/#>]')
	usr = 'admin'
	psw = ',j,heqcr'
	tln_sw_acc = telnetlib.Telnet(ip,23,5)
	tln_sw_acc.read_until("login :", 5)
	tln_sw_acc.write(usr + "\n")
	tln_sw_acc.read_until("password: ",5)
	tln_sw_acc.write(psw + "\n")
	data = tln_sw_acc.read_until(' /#', 5)
	tln_sw_acc.write("logout\n")
	tln_sw_acc.close()
	data_lst = data.splitlines()
	for i in range (len(data_lst)):
		fnd_sw_nm = rgx_nm.search(data_lst[i])
		if fnd_sw_nm is not None:
			fin_str = str(ip) + ' ' + str(fnd_sw_nm.group(1))
	return fin_str

print sw_acc(ip_sw)
