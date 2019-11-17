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
    q.sort(key=operator.attrgetter("deadline","entry"), reverse=True)
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
                    print("{0} {1} 1188 {2} {3}".format(entry+1, process.task, exec_time, header.power1188*exec_time))
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
                        print("{0} {1} 1188 {2} {3}".format(entry+1, next_process.task, exec_time, header.power1188*exec_time))
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
                    print ("{0} IDLE IDLE {1} {2}".format(seconds, next_entry - seconds, header.idle*(next_entry - seconds)))
                    entry = next_entry - 1
                    idle = True
        seconds += 1
        #Returns the tasks that were popped to the not ready list back to the queue 
        q = non_ready_task + q

def main(argv):
    inputFile = ''
    sched = ''
    EE = False 

    #Gathers all argument the user desires to use
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
    
    #Parses the input file of listed tasks 
    tasks, header = parse_tasks(inputFile)
    

    if(sched == 'edf'):
        edf(tasks, header)
    

if __name__== "__main__":
  main(sys.argv[1:])