import sys, getopt, operator
from Parser import Parser, Header


def Tasks(inputFile):
    tasks = [line.strip('\r\n').split(' ') for line in open(inputFile)]
    header = Header(tasks[0])
    print(header)
    return tasks

def Queue(tasks):
    q = []
    for t in tasks[1:]:
        q.append( Parser(t) )
    return q

def order(q):
    q.sort(key=operator.attrgetter("deadline"), reverse=True)

def edf(tasks, header):
    q = Queue(tasks)


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
    
    tasks = Tasks(inputFile)
    header = tasks[0]
    if(sched == 'edf'):
        edf(tasks, header)
    

if __name__== "__main__":
  main(sys.argv[1:])