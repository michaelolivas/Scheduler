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

def ee(tasks, header, sched):
    #initalize queue
    q = queue(tasks)
    #processes is a 2d list with this information: (power, hz, exe/deadline, wcet, task)
    processes = [[] for i in range(len(q))]
    #initialize rm inequality
    rm_ineq = float((float(len(q))*float((2**(1/float(len(q)))-1))))
    i=0
    #initialize processes and sorts them by least to greatest power
    for t in q:
        process_power_list=[]
        power = float(float(t.wcet1188)*float(header.power1188))
        process_power_list.append((power, 1188,float(float(t.wcet1188)/float(t.deadline)) ,t.wcet1188, t, header.power1188))
        power =  float(float(t.wcet918)*float(header.power918))
        process_power_list.append((power, 918,float(float(t.wcet918)/float(t.deadline)) ,t.wcet918, t, header.power918))
        power =  float(float(t.wcet648)*float(header.power648))
        process_power_list.append((power, 648,float(float(t.wcet648)/float(t.deadline)) ,t.wcet648, t, header.power648))
        power =  float(float(t.wcet384)*float(header.power384))
        process_power_list.append((power, 384,float(float(t.wcet384)/float(t.deadline)), t.wcet384, t, header.power384))
        process_power_list.sort()
        processes[i]=process_power_list
        i +=1
    ee_found = False
    #Algorithm for finding the most cost efficent schedule
    while not ee_found:
        inequality = 0
        #adds all the exce/deadline from the first index of least power
        for x in processes:
            inequality += x[0][2]
        #if not satisfies the inequality then reorganize the list by minimal change in exec/deadline
        if(inequality > 1 and sched == 'edf'):
            min = 1
            for x in processes:
                val = x[1][2] - x[0][2]
                if(val<min): 
                    min=val
                    next_hz = x
            save = next_hz[0]
            for i in range(len(next_hz)-1):
                next_hz[i] = next_hz[i+1]
            next_hz[len(next_hz)-1]=save
            continue
        ##if not satisfies the inequality then reorganize the list by minimal change in exec/deadline
        if(inequality > rm_ineq and sched =='rm'):
            min = 0
            for x in processes:
                val = x[1][2] - x[0][2]
                if(val<min): 
                    min=val
                    next_hz = x
            save = next_hz[0]
            for i in range(len(next_hz)-1):
                next_hz[i] = next_hz[i+1]
            next_hz[len(next_hz)-1]=save
            continue
        #if inequality is met, then assign hz, wcet, and power accordingly
        if(inequality <= 1 and sched == 'edf'):
            ee_list = []
            for x in processes:
                ee_list.append(x[0][4])
                x[0][4].hz = x[0][1]
                x[0][4].wcet = x[0][3]
                x[0][4].power = x[0][5]
            ee_found = True
        #if inequality is met, then assign hz, wcet, and power accordingly
        if(inequality <= rm_ineq and sched == 'rm'):
            ee_list = []
            for x in processes:
                ee_list.append(x[0][4])
                x[0][4].hz = x[0][1]
                x[0][4].wcet = x[0][3]
                x[0][4].power = x[0][5]
            ee_found = True
    #ONLY FOR RM: if it's possible to do an RM schedule then ee() will be called to re-organize the shcedule
    if(sched == 'rm'): rm(q, header, True, True, None)
    return ee_list


    
def edf(q, header, EE):
    non_ready_task = []
    num = len(q)
    entry = 0
    next_entry = 0
    idle = False
    exec_time = 0
    seconds = 0
    total_energy = 0
    total_idle = 0
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
                if(next_process.runTime == next_process.wcet):
                    print("{0} \t {1} \t {2} \t {3} \t {4}\t J".format(entry+1, process.task, process.hz, exec_time, process.power*exec_time))
                    total_energy +=  (process.power*exec_time)
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
                        print("{0} \t {1} \t {2} \t {3} \t {4}\t J".format(entry+1, next_process.task, next_process.hz, exec_time, next_process.power*exec_time))
                        total_energy += (next_process.power*exec_time)
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
                    total_idle += (next_entry - seconds)
                    entry = next_entry - 1
                    idle = True
        seconds += 1
        #Returns the tasks that were popped to the not ready list back to the queue 
        q = non_ready_task + q
    if(EE):
        print("Total Energy: {0}".format(total_energy))
        print("Idle time: {0} %".format(float(float(total_idle)/float(header.Exetime))*100))

def rm(q, header, EE, go_through, tasks):
    q = sort(q)
    num = len(q)
    schedule = [None] * header.Exetime #1,000 time units
    i = 0
    total_energy = 0
    total_idle = 0

    for task in q: #tasks in the queue
        start = task.entry #arrival time
        deadline = task.deadline #deadline
        execTime = task.wcet #execution time of the tasl
        for deads in range(deadline): # not sure lol
            #make sure time is within the arrival and deadline
            for time in range(start, deadline):
                deadlines = (start, deadline) #used for debugging, to make sure new start and end time was generated

                if (time <= deadline): # time is <= deadline
                    #for w4, first iteration: 57 + 0
                    #second iteration: 57 + 200, etc.
                    if (time < task.wcet + start): 
                        if (schedule[time] == None): # if there is an open spot in the schedule
                            schedule[time] = task.task #place task in open spot
                            execTime -= 1 #remaining execution time

                        elif (schedule[time] != None): #if spot is taken
                            start = time + 1
                            continue

                if (execTime == 0): #no more time to execute
                    execTime = task.wcet #reset execution time
                    #print (deadline, task.task, time + 1, execTime) #for debugging
                    if (time == len(schedule)): #if time reaches max size of schedule, reset to 0
                        time = 0
                        break
                    break

            if (execTime == 0):
                execTime = task.wcet #reset execution time to original time
                
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
    
    if(EE and not go_through):
        go_throuh = True
        return ee(tasks, header, 'rm')
    #IDLE states
    for i in range(len(schedule)):
        if (schedule[i] == None):
            schedule[i] = "IDLE"

    #printing
    for t in q:
        active_power = t.power
        hertz = t.hz
    start = 1
    burst = 0
    energy = 0
    idle_power = header.idle
    print ("start \t task \t hertz \t exec \t energy \n------------------------------------------")
    for key, data in groupby(schedule):
        burst = len(list(data))
        if (key == 'IDLE'):
            hertz = "IDLE"
            total_idle += burst
            energy = idle_power * burst
        else:
            hertz = t.hz
            energy = active_power * burst
            total_energy += energy
        print('{0} \t {1} \t {2} \t {3} \t {4}\tJ'.format(start, key , hertz, burst, energy))
        start += burst
    if(EE):
        print("Total Energy: {0}".format(total_energy))
        print("Idle time: {0} %".format(float(float(total_idle)/float(header.Exetime))*100))


def main(argv):
    inputFile = ''
    sched = ''
    EE = False 
    go_through = False
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
    q = queue(tasks)
    for x in q:
        x.power = header.power1188
    if(EE):
        if(sched == 'edf'):
            new_tasks = ee(tasks, header, sched)
            edf(new_tasks, header, EE)
        if(sched == 'rm'):
            rm(q,header, EE, go_through, tasks)
    elif(sched == 'edf'):
        edf(q, header,EE)
    elif(sched == 'rm'):
        rm(q, header, EE, go_through, tasks)
    
    

if __name__== "__main__":
  main(sys.argv[1:])
