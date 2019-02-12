#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import telnetlib
import re

#regular expressions

rgx_int_sta = re.compile('^([0-9\/]+)[ ]+([\S\/]+)[ ]+')
rgx_int_end = re.compile('[ ]+([\S]+)$')
rgx_vlan = re.compile('allowed vlan ([\S]+)')
rgx_arp_ip = re.compile('^([0-9.]+)[ ]')
rgx_arp_int = re.compile('Ethernet([\S]+)+[ ]')

# Incoming arguments

if len(sys.argv) == 4:
        host = sys.argv[1]
        user = sys.argv[2]
        passw = sys.argv[3]
else:
        print "The amount of attrib isn't correct."

# Function for access to switches
def sw_acc(ip):
        #fin_str = ' '
	fin_str2 = ' '
        #rgx_nm = re.compile('([A-Za-z0-9-.]+)[/#>]')
	rgx_sh_run= re.compile('^hostname ([\S]+)')
        usr = 'admin'
        psw = ',j,heqcr'
        try:
                tln_sw_acc = telnetlib.Telnet(ip,23,5)
                tln_sw_acc.read_until("login :", 5)
                tln_sw_acc.write(usr + "\n")
                tln_sw_acc.read_until("password: ",5)
                tln_sw_acc.write(psw + "\n")
                data = tln_sw_acc.read_until(' /#', 5)
		tln_sw_acc.write('sh run | include hostname\n')
		hst_nm = str(tln_sw_acc.read_until(' /#', 5)).splitlines()
		for i in range (len(hst_nm)):
			fnd_sw_hst_nm = rgx_sh_run.search(hst_nm[i])
			if fnd_sw_hst_nm is not None:
				fin_str2 = str(ip) + ' ' + str(fnd_sw_hst_nm.group(1))
                tln_sw_acc.write("logout\n")
                tln_sw_acc.close()
                #data_lst = data.splitlines()
                #for i in range (len(data_lst)):
                #       fnd_sw_nm = rgx_nm.search(data_lst[i])
                #        if fnd_sw_nm is not None:
                #                fin_str = str(ip) + ' ' + str(fnd_sw_nm.group(1))
        except Exception, e:
                #fin_str = str(ip) + ' FAIL'
		fin_str2 = str(ip) + ' FAIL'
                pass
        return fin_str2

tln = telnetlib.Telnet(host,23,5)
tln.read_until("login :", 5)
tln.write(user + "\n")
tln.read_until("password: ", 5)
tln.write(passw + "\n")
tln.write('terminal length 0\n')
tln.write('show interface ethernet status\n')
int_stats = str(tln.read_until(' >', 10)).splitlines()

#print int_stats

fin_lst = [' ']*len(int_stats)

for i in range (len(int_stats)):
	fnd_int = rgx_int_sta.search(int_stats[i])
	fnd_desc = rgx_int_end.search(int_stats[i])
	if fnd_int is not None:
		fin_lst[i] = [' ']*4
		fin_lst[i][0] = str(fnd_int.group(1))
	else:
		fin_lst[i] = [' ']*4
		fin_lst[i][0] = ' '
	if fnd_desc is not None:
		fin_lst[i][1] = str(fnd_desc.group(1))
	else:
		fin_lst[i][1] = ' '



print '------------------------------------------------\n'

for i in range (len(fin_lst)):
	if fin_lst[i][0] != ' ':
		tln.write('show run int eth  ' + str(fin_lst[i][0]) + '\n')
                vlan_data = str(tln.read_until(' >', 10)).splitlines()
		for j in range (len(vlan_data)):
			fnd_vl = rgx_vlan.search(vlan_data[j])
			if fnd_vl is not None:
				fin_lst[i][2] += str(fnd_vl.group(1))
		print 'Adding VIDs: ' + (" ".join(fin_lst[i]))


tln.write('show arp | include 10.102.\n')
arp_data = str(tln.read_until(' >', 10)).splitlines()

tln.write("logout\n")
tln.close()

for i in range (len(arp_data)):
        fnd_arp_ip = rgx_arp_ip.search(arp_data[i])
        fnd_arp_int = rgx_arp_int.search(arp_data[i])
        if fnd_arp_ip is not None and fnd_arp_int is not None:
                sw_ac_nm = str(sw_acc(fnd_arp_ip.group(1)))
                for j in range (len(fin_lst)):
                        if fin_lst[j][0] == str(fnd_arp_int.group(1)):
                                fin_lst[j][3] += ' ' + sw_ac_nm
                                print 'Adding SWs: ' + str((" ".join(fin_lst[j])))

print '++++++++++++++++++++++++++++++++++++++++++++++++++++++'
for i in range (len(fin_lst)):
	print ("\t".join(fin_lst[i]))
