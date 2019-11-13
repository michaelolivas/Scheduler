import sys, getopt, operator
from Parser import Parser, Header


def parse_tasks(inputFile):
    tasks = [line.strip('\r\n').split(' ') for line in open(inputFile)]
    header = Header(tasks[0])
    return tasks, header

def queue(tasks):
    q = []
    for t in tasks[1:]:
        q.append( Parser(t) )
    return q

def sort_edf(q):
    q.sort(key=operator.attrgetter("deadline", "wcet1188"), reverse=True)
    return q

def edf(tasks, header):
    q = queue(tasks)
    num = len(q)
    power = header.power1188 * 0.001
    exe_time = 0
    for sec in range(header.Exetime):
        idle = False 
        new_process = False      
        q = sort_edf(q)
        pull = []
        for i in range(num):
            process = q.pop()
            if(sec == 0 ): previous_process = process
            if(previous_process == process):
                break
            if (previous_process != process):
                new_process = True
                previous_process = process
            if(process.entry > sec):
                pull.append(process)
                if(i == num-1):
                    idle = True
                    break
            if(process.entry <= sec):
                pull.append(process)
                break
        if(previous_process == process and not new_process):
            exe_time = exe_time + 1
        if(new_process):
            previous_process.runTime = previous_process.runTime + 1
            print(sec, previous_process.task, exe_time)
            exe_time = 0
        if(idle):
            q = pull + q 
            print("{0} IDLE {1}".format(sec, sec+1))
            continue

        if (process.runTime == process.wcet1188):
            process.runTime = 0
            process.entry = process.deadline
            process.deadline = process.deadline + process.period

        q = pull + q


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
    
    tasks, header = parse_tasks(inputFile)
    
    if(sched == 'edf'):
        edf(tasks, header)
    

if __name__== "__main__":
  main(sys.argv[1:])