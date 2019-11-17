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

def sort_edf(q): #sort when using pop()
    q.sort(key=operator.attrgetter("deadline", "wcet1188"), reverse=True)
    return q

def sort(q): #sort without pop()
    q.sort(key=operator.attrgetter("deadline", "wcet1188"))
    return q

def edf(tasks, header):
    q = queue(tasks)
    num = len(q)
    power = header.power1188
    print(power)
    for sec in range(header.Exetime): 
        idle = False       
        q = sort_edf(q)
        pull = []
        for i in range(num):
            process = q.pop()
            if(process.entry > sec):
                pull.append(process)
                if(i == num-1):
                    idle = True
                    break
                
            if(process.entry <= sec):
                pull.append(process)
                break
        if(idle):
            q = pull + q 
            print("{0} IDLE {1}".format(sec, sec+1))
            continue
        if(process.entry <= sec):
            process.runTime = process.runTime + 1
            print(sec, process.task, process.runTime+sec)
        if (process.runTime == process.wcet1188):
            process.runTime = 0
            process.entry = process.deadline
            process.deadline = process.deadline + process.period
        q = pull + q

def rm(tasks, header):
    q = queue(tasks)
    q = sort(q)
    num = len(q)
    schedule = [None] * header.Exetime #1,000 time units

    i = 0
    for task in q:
        start = task.entry
        deadline = task.deadline
        execTime = task.wcet1188
        for deads in range(deadline):
            deadlines = (start, deadline)
            for time in range(start, deadline):
                if (time <= deadline):
                    if (time < task.wcet1188 + start):
                        if (schedule[time] == None):
                            schedule[time] = task.task
                            execTime -= 1
                            print (task.task, time)
                        if (schedule[time] != None):
                            break
            if (execTime < 0):
                execTime = task.wcet1188
                if (time == len(schedule)):
                    break
            start = deadline
            deadline += task.deadline
            deadlines = (start, deadline)
            time = start
            if (time == len(schedule)):
                    break
        if (time == len(schedule)):
            time = 0
        print(schedule)

        



    #Create a deadline list in the format (start, deadline)
        
        # for deadline in deadlines:
        #     start, deadline = deadline
        #     for time in range(start, deadline):
        #         if check none:
        #             replace 


        
            
            
        


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
    if(sched == 'rm'):
        rm(tasks, header)
    

if __name__== "__main__":
  main(sys.argv[1:])