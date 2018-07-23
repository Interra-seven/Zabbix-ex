#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import telnetlib
import re
import time

fin_lst = []
rgx_chg = re.compile('Battery charge[ ]+: ([0-9.]+)')
rgx_ld = re.compile('Load[ ]+: ([0-9.]+)')
rgx_vac = re.compile('Input voltage[ ]+: ([0-9.]+)')



if len(sys.argv) == 2:
	tln = telnetlib.Telnet(sys.argv[1], 50 , 10)
	time.sleep(3)
	tln.write('\r\n')
	data = (str(tln.read_until('>', 30))).split("\r\n")
	tln.close()
	for i in range (len(data)):
		fnd_chg = rgx_chg.search(data[i])
		fnd_ld = rgx_ld.search(data[i])
		fnd_vac = rgx_vac.search(data[i])
		if fnd_chg != None:
			fin_lst.append('Battery charge: ' + str(fnd_chg.group(1)))
		if fnd_ld != None:
			fin_lst.append(' battery load: ' + str(fnd_ld.group(1)))
		if fnd_vac != None:
			fin_lst.append(' input VAC: ' + str(fnd_vac.group(1)))
	print (" ".join(fin_lst)) + "\n"
	log_f = open('/var/log/krv-apc1000x.log', 'a')
	log_f.write(str(time.strftime('%d-%m-%Y %H:%M:%S')) + " " + (" ".join(fin_lst)) + "\n")
	log_f.close()
else:
	"The amount of attrib isn't correct!"

