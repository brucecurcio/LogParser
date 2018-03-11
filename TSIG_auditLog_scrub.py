#!/usr/bin/env python
'''
This Python script is used to parse the audit log for NSGroup Modified messages.

  it will determine what is being added and taken away in each message

'''


import sys
import os
import time
import datetime
import csv


def main():
    in_file = open('audit.log.0', 'r')
    auditFile = str(in_file.readlines())
    in_file.close()

    extPriLoc = auditFile.find("external_primaries")
    extSecLoc = auditFile.find("external_secondaries")

    extPrim = auditFile[extPriLoc:extSecLoc]
    beforeArrowPri = extPrim.find("->")
    extPrimCurrent = extPrim[20:beforeArrowPri-1]
    extPrimChange = extPrim[beforeArrowPri+3:-2]
    extPrimCurrSet = set(extPrimCurrent.split("]"))
    extPrimChgSet = set(extPrimChange.split("]"))
    extPrimAdd = extPrimCurrSet.union(extPrimChgSet) - extPrimCurrSet
    extPrimDelete = extPrimCurrSet.union(extPrimChgSet) - extPrimChgSet

    extSec = auditFile[extSecLoc:]
    beforeArrowSec = extSec.find("->")
    extSecCurrent = extSec[22:beforeArrowSec-1]
    extSecChange = extSec[beforeArrowSec+3:-5]
    extSecCurrSet = set(extSecCurrent.split("]"))
    extSecChgSet = set(extSecChange.split("]"))
    extSecAdd = extSecCurrSet.union(extSecChgSet) - extSecCurrSet
    extSecDelete = extSecCurrSet.union(extSecChgSet) - extSecChgSet

#    print ("wholefile " + auditFile)
#    print("extPrimCurrent " + extPrimCurrent)
#    print("extPrimChange " + extPrimChange)
#    print("extSecCurrent " + extSecCurrent)
#    print("extSecChange " + extSecChange)
#    print(extPrimCurrSet)
#    print(extPrimChgSet)
#    print(extPrimAdd)
#    print(extPrimDelete)
    print(extSecCurrSet)
    print(extSecChgSet)
    print(extSecAdd)
    print(extSecDelete)

if __name__ == "__main__":
    main()
