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
    beforeArrow = extPrim.find("->")
    extPrimCurrent = extPrim[18:beforeArrow]
    extPrimChange = extPrim[beforeArrow+2:]


#    extSecCurrent =
#    extSecChange

    print(auditFile)
    print(extPrimCurrent)
    print(extPrimChange)

if __name__ == "__main__":
    main()
