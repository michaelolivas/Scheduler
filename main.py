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
    for task in q: #tasks in the queue
        start = task.entry #arrival time
        deadline = task.deadline #deadline
        execTime = task.wcet1188 #execution time of the tasl
        for deads in range(deadline): # not sure lol
            deadlines = (start, deadline)
            for time in range(start, deadline): #make sure time is within the arrival and deadline
                deadlines = (start, deadline)
                if (time <= deadline): # time is <= deadline
                    #for w4, first iteration: 57 + 0
                    #second iteration: 57 + 200, etc.
                    if (time < task.wcet1188 + start): 
                        if (schedule[time] == None): # if there is an open spot in the schedule
                            schedule[time] = task.task #place task in open spot
                            execTime -= 1 #remaining execution time
                            print (deadline, task.task, time + 1, execTime) #for debugging
                        elif (schedule[time] != None): #if spot is taken
                            start = time + 1
                            # if (execTime != 0):
                            #     print ("Scheduling Failed at time {0}".format(time))
                            #     exit(1)
                            continue
                if (execTime == 0): #no more time to execute
                    execTime = task.wcet1188 #reset execution time
                    if (time == len(schedule)): #if time reaches max size of schedule, reset to 0
                        time = 0
                        break
                    break
                # if (time == len(schedule)):
                #     time = 0
            if (execTime == 0):
                execTime = task.wcet1188
            # if (execTime != 0 and time < start):
            #     print ("Scheduling Failed at time {0}".format(time))
            #     exit(1)
            start = deadline #reassign arrival/start time
            deadline += task.deadline #reassign deadline
            deadlines = (start, deadline) #put back in tuple
            time = start #make new start time
            if (deadline >= len(schedule)): #if the deadline time is mroe than 1000
                deadline = len(schedule) #make final deadline 1000
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