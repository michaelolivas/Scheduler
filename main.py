import pandas as pd
import json
import sys, getopt
import numpy as np
from Parser import Parser


def Tasks(inputFile):
    tasks = [line.strip('\r\n').split(' ') for line in open(inputFile)]
    print(tasks[1])
    return tasks
        

def main(argv):
    inputFile = ''
    
    try:
        opts, arg = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg

    tasks = Tasks(inputFile)
    W1 = Parser(tasks[1])
    print(W1)

if __name__== "__main__":
  main(sys.argv[1:])