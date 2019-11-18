import sys, getopt, operator
from Parser import Parser, Header
from itertools import groupby


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
    q.sort(key=operator.attrgetter("deadline","entry"), reverse=True)
    return q

def sort(q): #sort without pop()
    q.sort(key=operator.attrgetter("deadline", "entry"))
    return q

def edf(tasks, header):
    q = queue(tasks)
    non_ready_task = []
    num = len(q)
    entry = 0
    next_entry = 0
    idle = False
    exec_time = 0
    seconds = 0
    print ("start \t task \t hertz \t exec \t energy \n------------------------------------------")
    #Runs for the entire execution time desired
    while seconds < header.Exetime:
        #If it's Idle, stay Idle until next available entry
        if(idle):
            if(seconds < next_entry): 
                seconds += 1
                continue 
        #Reset for checking purposes     
        idle = False

        q = sort_edf(q)
        non_ready_task = []
        #Sorts through the queue in order to see which task to run next
        for x in range(num):
            process = q.pop()
            if(seconds == 0): next_process = process
            if(x == 0): next_entry = process.entry
            #Checks if it's time for the process to be executed
            if(process.entry <= seconds):
                process.runTime = process.runTime + 1
                exec_time +=1  
                #Checks if the process has reached it's execution time
                if(next_process.runTime == next_process.wcet1188):
                    print("{0} \t {1} \t 1188 \t {2} \t {3}\t J".format(entry+1, process.task, exec_time, header.power1188*exec_time))
                    entry = entry+exec_time
                    seconds = entry
                    exec_time = 0
                    process.runTime = 0
                    process.entry += process.period
                    process.deadline = process.deadline + process.period
                    non_ready_task.append(process)
                    break
                #Checks if a new process is being executed
                elif(next_process != process): 
                    if(exec_time != 1):
                        exec_time -=1
                        print("{0} \t {1} \t 1188 \t {2} \t {3}\t J".format(entry+1, next_process.task, exec_time, header.power1188*exec_time))
                        entry = entry+exec_time
                        seconds = entry
                        exec_time = 1
                    next_process = process
                    non_ready_task.append(process)
                    break
                non_ready_task.append(process)
                break
            #If the process next in the que is not ready
            if(process.entry > seconds):
                #Adds to the not ready list, and on  the top of the loop pops the next process 
                non_ready_task.append(process)
                #If it has checked the whole queue then, all asks are not ready. Therefore, Idle.
                if(x == num -1): 
                    print ("{0} \t IDLE \t IDLE \t {1} \t {2}\t J".format(seconds, next_entry - seconds, header.idle*(next_entry - seconds)))
                    entry = next_entry - 1
                    idle = True
        seconds += 1
        #Returns the tasks that were popped to the not ready list back to the queue 
        q = non_ready_task + q

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
            #make sure time is within the arrival and deadline
            for time in range(start, deadline):
                deadlines = (start, deadline) #used for debugging, to make sure new start and end time was generated

                if (time <= deadline): # time is <= deadline
                    #for w4, first iteration: 57 + 0
                    #second iteration: 57 + 200, etc.
                    if (time < task.wcet1188 + start): 
                        if (schedule[time] == None): # if there is an open spot in the schedule
                            schedule[time] = task.task #place task in open spot
                            execTime -= 1 #remaining execution time

                        elif (schedule[time] != None): #if spot is taken
                            start = time + 1
                            continue

                if (execTime == 0): #no more time to execute
                    execTime = task.wcet1188 #reset execution time
                    #print (deadline, task.task, time + 1, execTime) #for debugging
                    if (time == len(schedule)): #if time reaches max size of schedule, reset to 0
                        time = 0
                        break
                    break

            if (execTime == 0):
                execTime = task.wcet1188 #reset execution time to original time
                
            if (execTime != 0 and time < start): #if end of schedule length is reached, reset time counter
                if (time == len(schedule) - 1):
                    time = 0
                    break
                else: #if scheduling fails
                    print ("\n---------Scheduling Failed at time {0}---------\n".format(time))
                    exit(1)

            start = deadline #reassign arrival/start time
            deadline += task.deadline #reassign deadline
            deadlines = (start, deadline) #put back in tuple
            time = start #make new start time

            if (deadline >= len(schedule)): #if the deadline time is mroe than 1000
                deadline = len(schedule) #make final deadline 1000
    
    #IDLE states
    for i in range(len(schedule)):
        if (schedule[i] == None):
            schedule[i] = "IDLE"

    #printing
    start = 1
    burst = 0
    active_power = header.power1188
    energy = 0
    idle_power = header.idle
    print ("start \t task \t hertz \t exec \t energy \n------------------------------------------")
    for key, data in groupby(schedule):
        burst = len(list(data))
        if (key == 'IDLE'):
            hertz = "IDLE"
            energy = idle_power * burst
        else:
            hertz = 1188
            energy = active_power * burst
        print('{0} \t {1} \t {2} \t {3} \t {4}\tJ'.format(start, key , hertz, burst, energy))
        start += burst


def main(argv):
    inputFile = ''
    sched = ''
    EE = False 

    #Gathers all argument the user desires to use
    try:
        opts, arg = getopt.getopt(argv,"hi:s:e", ["help","inFile=", "schedule=", "energy"])
    except getopt.GetoptError:
        print ('main.py -i <inputfile> -s <edf/rm> -e')
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
    
    #Parses the input file of listed tasks 
    tasks, header = parse_tasks(inputFile)
    

    if(sched == 'edf'):
        edf(tasks, header)
    if(sched == 'rm'):
        rm(tasks, header)
    

if __name__== "__main__":
  main(sys.argv[1:])