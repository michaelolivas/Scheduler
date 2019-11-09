import sys, getopt
import numpy as np
from Parser import Parser


def Tasks(inputFile):
    tasks = [line.strip('\r\n').split(' ') for line in open(inputFile)]
    work = [Parser(tasks[x]) for x in range(len(tasks))]
    return tasks, work
        

def main(argv):
    inputFile = ''
    sched = ''
    EE = False 
    task = []
    work = []

    try:
        opts, arg = getopt.getopt(argv,"hi:s:e", ["help","inFile=", "schedule=", "energy"])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -s <edf/rm> -e')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print ('test.py -i <inputfile> -s <edf/rm> -e')
            sys.exit()
        if opt in ("-i", "--ifile"):
            inputFile = arg
        if opt in ("-s", "--schedule"):
            sched = arg
        if opt in ("-e", "--energy"):
            EE = True

    tasks , work = Tasks(inputFile)

if __name__== "__main__":
  main(sys.argv[1:])