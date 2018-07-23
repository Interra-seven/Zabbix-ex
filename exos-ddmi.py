#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import telnetlib
import re

lst_fin = []
rgx = re.compile('^([0-9]+)[ ]+([0-9.]+)[ ]+([0-9.-]+)[ ]+([0-9.-]+)')

if len(sys.argv) == 4:
        tln = telnetlib.Telnet(sys.argv[1],23,5)
        tln.read_until("login :", 5)
        tln.write(sys.argv[2] + "\n")
        tln.read_until("password: ",5)
        tln.write(sys.argv[3] + "\n")
        tln.write('show ports transceiver information | exclude ignore-case [this]\n')
        data = str(tln.read_until(' >',5))
        data2 = (str(tln.read_until(' >',5))).split("\r\n")
        tln.write("logout\n")
        tln.close()
	for i in range (len(data2)):
		fnd = rgx.search(data2[i])
		if fnd != None:
			lst_fin.append('Port ' + str(fnd.group(1)) + ' temp ' + str(fnd.group(2)))
			lst_fin.append(' tx ' + str(fnd.group(3)) + ' rx ' + str(fnd.group(4)))
	print (" ".join(lst_fin))
else:
        print "The amount of attributes isn't correct"

