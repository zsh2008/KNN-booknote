# -*- coding: windows-1252 -*-

""" used for monitor board if reset during
    security test

modify history:
    2017.03.27:
        1 First version .
"""

__author__ = "Brown Zhao (Brown.Zhao@alcatel-lucent.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2017/03/27 17:29:20 $"
__license__ = "Python"

import xml.etree.ElementTree as ET

from lib_common.lib_common import *


def xml_parse():
    cli = cli_libs()
    cmd = "show equipment slot xml"
    cmdresult = cli.send_telCmd(cmd)
    slot = {}
    actual_type = {}
    oper_status = {}
    err_status = {}
    availability = {}
    lt_restart_num = {}
    slot_num = 1
    actual_num = 1
    oper_num = 1
    err_num = 1
    ava_num = 1
    rest_num = 1
    # put out the xml show into a file to make it becomes an available xml file
    cmdneed1 = re.findall(r"<\?xml.*static\">", cmdresult, re.S)
    cmdneed2 = re.findall(r"<instance.*/instance>", cmdresult, re.S)
    cmdneed3 = re.findall(r"</hierarchy.*/runtime-data>", cmdresult, re.S)
    cmdneed = cmdneed1+cmdneed2+cmdneed3
    print cmdneed

    f = open('cmdresfile','w+')
    for cmd in cmdneed:
        f.write(cmd)
    f.close()
    f = open('cmdresfile', 'rt')
    tree = ET.parse(f)

    # below function to parse the xmlbody's value
    list_slot = []
    dic_slot = {}
    for instance in tree.iter("res-id"):
        #slot[slot_num] = instance.text
        #slot_num = slot_num + 1
        #dic_slot[slot-id] = instance.txt
        for instance in tree.iter("info"):
            if instance.attrib['name'] == "lt-restart-num":
                lt_restart_num[rest_num] = instance.text
                rest_num = rest_num +1
            elif instance.attrib['name'] == "actual-type":
                actual_type[actual_num] = instance.text
                actual_num = actual_num + 1
            elif instance.attrib['name'] == "oper-status":
                oper_status[oper_num] = instance.text
                oper_num = oper_num + 1
            elif instance.attrib['name'] == "error-status":
                err_status[err_num] = instance.text
                err_num = err_num + 1
            elif instance.attrib['name'] == "availability":
                availability[ava_num] = instance.text
                ava_num = ava_num + 1
        #print dict_slot
    f.close()
    #print slot.values(), actual_type.values(), oper_status.values(), err_status.values(),
    #availability.values()
    #print lt_restart_num.values()

    for value in lt_restart_num.keys():
        if int(lt_restart_num[value]) > 0:
            print "The board %s, restart num : %s" %(actual_type[value], lt_restart_num[value])




if __name__=='__main__':
    xml_parse()