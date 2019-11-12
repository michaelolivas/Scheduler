import copy, operator
from itertools import groupby
<<<<<<< HEAD
from Queue import PriorityQueue
from Parser import Parser
=======
import Parser as task
>>>>>>> started EDF, doesn't work


class MyPriorityQueue(PriorityQueue, Parser):
    def __init__ (self):
        self.q = []

    def put(self, object):
        self.q.append(Parser(object))
    
    def cmp_priority(a, b):
        return cmp(a.deadline, b.deadline)

    def sort(self):
        self.q.sort(key=operator.attrgetter("deadline"))

    def get(self):
        return self.q.pop()
    
    def __str__(self):
        for l in self.q:
            Parser.__str__(l)
            print('\n')
'''
class Scheduling(object):
    def __init__ (self, num_tasks: int, exec_time: int, p1188MHz: int, p918MHz: int,
                p648MHz: int, p384MHz: int, p_idle: int, type_sch: str, EnEff: bool):

        self.num_tasks = int(num_tasks)
        self.exec_time = int(exec_time)
        self.p1188MHz = int(p1188MHz)
        self.p918MHz = int(p918MHz)
        self.p648MHz = int(p648MHz)
        self.p384MHz = int(p384MHz)
        self.p_idle = int(p_idle)
        self.type_sch = type_sch
        self.EnEff = EnEff

    def schedule(self, task):
        if self.type_sch.lower == 'edf' and self.EnEff is False:
            self.edf(task)
        if self.type_sch.lower == 'rm' and self.EnEff is False:
            self.rm(task)
        if self.type_sch.lower == 'edf' and self.EnEff is True:
            self.edf_EnEff(task)
        if self.type_sch.lower == 'rm' and self.EnEff is True:
            self.rm_EnEff(task)



    def edf(self, task):
        queue = [] #task queue
        schedule = [] #output schedule
        current = '' #current task
        previous = '' #previous task

        for time in range (task[1]):
            for t in task.keys():
                if time == task[2]:
                    queue.append(t)
        return schedule


    def rm(self, task):
        pass

    def edf_EnEff(self, task):
        pass

    def rm_EnEff(self, task):
        pass
'''