#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
from shutil import copyfile
import sys
import csv

def readHerbList():
    herblist = []
    rows = csv.reader(open("./herblist-21-04-16.csv", "rb"))
    for row in rows:
        herblist.append(row[1].strip())
    return herblist

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./symptoms-21-04-16.csv", "rb"))
    for row in rows:
        symptoms.append(row[1].strip())
    return symptoms

def filterDocument(filepath, destination_dir, filename, herblist, symptoms):
    src_file = open(filepath+"/"+filename, 'r')
    src = filepath+"/"+filename
    dst = destination_dir+"/"+filename

    print "\nprocessing ",filename," : ",

    flagHerb = False
    flagSymptoms = False
    flagProp = False
    msg = ''

    for line in iter(src_file):
        words = line.split("|")
        for word in words:
            if word in herblist:
                msg = "herb : "+word
                flagHerb = True
                break
        if flagHerb:
            break

    if flagHerb:
        for line in iter(src_file):
            words = line.split("|")
            for word in words:
                if word in symptoms:
                    msg = msg+", symp : "+word
                    flagSymptoms = True
                    copyfile(src, dst)
                    break
            if flagSymptoms:
                break

    src_file.close()
    if flagHerb and flagSymptoms:
        print msg,
    else:
        print "not found : "+msg

def main():
    herblist = readHerbList()
    symptoms = readSymptoms()
    propoties = readProperties()
    if len(sys.argv) != 1:
        filedir = sys.argv[1]

        upone_level = path.dirname(filedir.rstrip('/'))
        destination_dir = upone_level+"/filtered3"

        # Create directory for store result file
        if not path.exists(destination_dir):
            makedirs(destination_dir)

        # List all file from target directory
        onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]
        for filename in onlyfiles:
            filterDocument(filedir, \
                            destination_dir, \
                            filename, \
                            herblist, \
                            symptoms)
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()

