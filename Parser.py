import pandas as pd
import json
import sys, getopt


class Parser:
    def __init__(self, input_txt):
        self.input_txt = input_txt
        txt = [line.rstrip('\n') for line in open(input_txt)]
        W1 = txt[1]
        W1 =W1.split("w1")[-1]
        W1 = W1.split()
        print(W1)  

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

    print(inputFile)
    test = Parser(inputFile)


if __name__== "__main__":
  main(sys.argv[1:])

