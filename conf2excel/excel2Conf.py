#!/usr/bin/python
# Python Script to convert a excel sheet to conf
####
__author__ = 'Dinoop Balakrishnan'
__version__ = '0.0.1'


import os,sys

def fileExists(fName):
    status =""
    try:
      with open(fName) as f: 
        status='File Exists' 
        return True,status
    except IOError as e:
      return False,e

def main(excelName):
  xlExists, status = fileExists(excelName)
  if xlExists:
    print status
  else:
    print status


if __name__ == "__main__":
  main(sys.argv[1])
