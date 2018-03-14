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
import re
import glob


def NSGLogExtractor(logFile):

    in_file = open(logFile, 'r')
    auditFile = in_file.readlines()
    in_file.close()

    nsgModEntries = []

    for line in auditFile:
        if 'Modified NsGroup' in line:
            nsgModEntries.append(line)

#    print(nsgModEntries[600])
    return nsgModEntries

def ExtractEntry(auditList):
    entry = str(auditList)
#    print(entry)

    date = entry[0:24]
#    print(date)

    nameGrp = re.search('Modified NsGroup (.*?):', entry).group(0)
#    print(nameGrp)

    action = re.search('Changed (.*?):', entry).group(0)
#    print(action)

    fh = open("nsgChgFile.txt", "a")
    fh.write(date + " | " + nameGrp + " | " + action + "\n")
    fh.close()

    print(date + " | " + nameGrp + " | " + action)

def DeltaLocator(auditEntry):

    entryString = str(auditEntry)

    extPri = re.search('external_primaries:\[\[(.*?)external_secondaries', entryString).group(0)
#    print (extPri)

    extSec = re.search('external_secondaries(.*$)', entryString).group(0)
#    print(extSec)

    extPriCurr = re.search('name(.*?)->', extPri).group(0)
    extPriChg = re.search('->(.*$)', extPri).group(0)
    #print(extPriCurr)
    #print(extPriChg)

    extPriCurrList = re.findall('name=\"(.*?\".*?\".*?)\"', extPriCurr)
    #    print(extPriCurrList)
    extPriChgList = re.findall('name=\"(.*?\".*?\".*?)\"', extPriChg)
    #    print(extPriChgList)

    extPriCurrSet = set(extPriCurrList)
    extPriChgSet = set(extPriChgList)

    extPriAdd = extPriCurrSet.union(extPriChgSet) - extPriCurrSet
    extPriDelete = extPriCurrSet.union(extPriChgSet) - extPriChgSet
    print("Added Ext Primaries " + str(extPriAdd))
    print("Deleted Ext Primaries " + str(extPriDelete))


    extSecCurr = re.search('name(.*?)->', extSec).group(0)
    extSecChg = re.search('->(.*$)', extSec).group(0)
    #print(extSecCurr)
    #print(extSecChg)



    extSecCurrList = re.findall('name=\"(.*?\".*?\".*?)\"', extSecCurr)
    extSecChgList = re.findall('name=\"(.*?\".*?\".*?)\"', extSecChg)

    extSecCurrSet = set(extSecCurrList)
    extSecChgSet = set(extSecChgList)

    extSecAdd = extSecCurrSet.union(extSecChgSet) - extSecCurrSet
    extSecDelete = extSecCurrSet.union(extSecChgSet) - extSecChgSet
    print("Added Ext Secondaries " + str(extSecAdd))
    print("Deleted Ext Secondaries " + str(extSecDelete))

    fh = open("nsgChgFile.txt", "a")
    if (extPriAdd != set()):
        fh.write("Added Ext Primaries " + str(extPriAdd) + "\n")
    if (extPriDelete != set()):
        fh.write("Deleted Ext Primaries " + str(extPriDelete) + "\n")
    if (extSecAdd != set()):
        fh.write("Added Ext Secondaries " + str(extSecAdd) + "\n")
    if (extSecDelete != set()):
        fh.write("Deleted Ext Secondaries " + str(extSecDelete) + "\n")
    fh.write("\n")
    fh.close()

    extSecCurrList = re.findall('name=\"(.*?\".*?\".*?)\"', extSecCurr)
#    print(extSecCurrList)
    extSecChgList = re.findall('name=\"(.*?\".*?\".*?)\"', extSecChg)
#    print(extSecChgList)


    # extPriLoc = auditEntry.find("external_primaries")
#    extSecLoc = auditEntry.find("external_secondaries")

#    extPrim = auditEntry[extPriLoc:extSecLoc]
#    beforeArrowPri = extPrim.find("->")
#    extPrimCurrent = extPrim[20:beforeArrowPri-1]
#    extPrimChange = extPrim[beforeArrowPri+3:-2]
#    extPrimCurrSet = set(extPrimCurrent.split("]"))
#    extPrimChgSet = set(extPrimChange.split("]"))
#    extPrimAdd = extPrimCurrSet.union(extPrimChgSet) - extPrimCurrSet
#    extPrimDelete = extPrimCurrSet.union(extPrimChgSet) - extPrimChgSet

#    extSec = auditEntry[extSecLoc:]
#    beforeArrowSec = extSec.find("->")
#    extSecCurrent = extSec[22:beforeArrowSec-1]
#    extSecChange = extSec[beforeArrowSec+3:-5]
#    extSecCurrSet = set(extSecCurrent.split("]"))
#    extSecChgSet = set(extSecChange.split("]"))
#    extSecAdd = extSecCurrSet.union(extSecChgSet) - extSecCurrSet
#    extSecDelete = extSecCurrSet.union(extSecChgSet) - extSecChgSet

#    print ("wholefile " + auditEntry)
#    print("extPrimCurrent " + extPrimCurrent)
#    print("extPrimChange " + extPrimChange)
#    print("extSecCurrent " + extSecCurrent)
#    print("extSecChange " + extSecChange)
#    print(extPrimCurrSet)
#    print(extPrimChgSet)
#    print("added Primaries "+str(extPrimAdd))
#    print("deleted Primaries "+str(extPrimDelete))
#    print(extSecCurrSet)
#    print(extSecChgSet)
#    print("added Secondaries "+str(extSecAdd))
#    print("deleted Secondaries "+str(extSecDelete))
    print("")

def main():

    os.chdir("./")
    for file in glob.glob("audit*"):
        print(file)
        logEntries = NSGLogExtractor(file)
        for line in logEntries:
            ExtractEntry(line)
            DeltaLocator(line)

if __name__ == "__main__":
    main()
