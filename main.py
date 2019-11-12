import sys, getopt, operator
from Parser import Parser, Header


def Tasks(inputFile):
    tasks = [line.strip('\r\n').split(' ') for line in open(inputFile)]
    header = Header(tasks[0])
    return tasks, header

def Queue(tasks):
    q = []
    for t in tasks[1:]:
        q.append( Parser(t) )
    return q

def order(q):
    q.sort(key=operator.attrgetter("deadline"), reverse=True)
    return q

def edf(tasks, header):
    q = Queue(tasks)
    q = order(q)
    for sec in range(header.Exetime):
        q = order(q)
        process = q.pop()
        if(process.entry > sec):
            print("{0} IDLE {1}".format(sec, sec+1))
        if(process.entry <= sec):
            process.runTime = process.runTime + 1
            print(sec, process.task, process.runTime+sec)
        if (process.runTime == process.wcet1188):
            process.runTime = 0
            process.entry = process.entry + process.deadline
            process.deadline = process.deadline + process.entry
        
        q.append(process)

def main(argv):
    inputFile = ''
    sched = ''
    EE = False 

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
    
    tasks, header = Tasks(inputFile)
    
    if(sched == 'edf'):
        edf(tasks, header)
    

if __name__== "__main__":
  main(sys.argv[1:])