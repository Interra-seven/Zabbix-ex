#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import telnetlib
import re

#regular expression
rgx_int = re.compile('^([0-9]+)[ ]+([A-Za-z-0-9-]+)')
rgx_vid = re.compile('^[A-Za-z0-9-]+[ ]+([0-9]+)')
rgx_ip_port = re.compile(' ([0-9]+)$')
rgx_ip_ip = re.compile('(10.[0-9]+.[0-9]+.[0-9]+)')

# Incoming arguments
if len(sys.argv) == 4:
	host = sys.argv[1]
	user = sys.argv[2]
	passw = sys.argv[3]
else:
	print "The amount of attrib isn't correct."

# Function for access to switches
def sw_acc(ip):
	fin_str = ' '
        rgx_nm = re.compile('([A-Za-z0-9-.]+)[/#>]')
        usr = 'admin'
        psw = ',j,heqcr'
	try:
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
	except Exception, e:
		fin_str = str(ip) + ' FAIL'
		pass
	return fin_str

tln = telnetlib.Telnet(host,23,5)
tln.read_until("login :", 5)
tln.write(user + "\n")
tln.read_until("password: ",5)
tln.write(passw + "\n")
tln.write('disable clipaging\n')
tln.write('show ports no-refresh | include 1000\n')
data = str(tln.read_until(' >',5))
#print data
data2 = str(tln.read_until(' >',5))
#print data2
data3 = str(tln.read_until(' >',15))
print data3
data4 = data3.splitlines()
#print data4
fin_lst = [' ']*len(data4)
for i in range (len(data4)):
	fnd = rgx_int.search(data4[i])
	if fnd is not None:
		fin_lst[i] = [' ']*4
		fin_lst[i][0] = str(fnd.group(1))
		fin_lst[i][1] = str(fnd.group(2))
	else:
		fin_lst[i] = [' ']*4

print '------------------------------------------------------'
vlan_lst = []

for i in range (len(fin_lst)):
	if fin_lst[i][0] != ' ':
		tln.write('show vlan ports ' + str(fin_lst[i][0]) + ' | include ANY\n')
		vlan_data = str(tln.read_until(' >', 10))
		#print vlan_data
		vlan_data_str = vlan_data.splitlines()
		for j in range (len(vlan_data_str)):
			vlan_fnd = rgx_vid.search(vlan_data_str[j])
			if vlan_fnd is not None:
				fin_lst[i][2] += str(vlan_fnd.group(1)) + ' '
			#print fin_lst[i][2]
		print 'Adding vlans VID...\n ' + (" ".join(fin_lst[i]))

tln.write('show iparp | include 10.101\n')
iparp_data = str(tln.read_until(' >', 20))

tln.write("logout\n")
tln.close()

for i in range (len(fin_lst)):
	#if fin_lst[i][0] is not None:
	#	print (" ".join(fin_lst[i]))
	print fin_lst[i]
print '------------------------------------------------------'
#port = 0
ip_arp_data_str = iparp_data.splitlines()
for i in range (len(ip_arp_data_str)):
	fnd_ip = rgx_ip_ip.search(ip_arp_data_str[i])
	fnd_port = rgx_ip_port.search(ip_arp_data_str[i])
	if fnd_port is not None:
		port = int(fnd_port.group(1))
		print 'Port >>> ' + str(port)
		if fnd_ip != None:
			str_ip_hostname = str(sw_acc(fnd_ip.group(1)))
			print 'String ip-hostname ' + str_ip_hostname
			for j in range (len(fin_lst)):
				if fin_lst[j][0] != ' ':
					val = int(fin_lst[j][0])
					if val  == port:
						fin_lst[j][3] += str_ip_hostname + ' '
				#print fin_lst[j]

for i in range (len(fin_lst)):
        print (" ".join(fin_lst[i]))

