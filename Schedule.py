import copy
from itertools import groupby

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
        pass

    def rm(self, task):
        pass

    def edf_EnEff(self, task):
        pass

    def rm_EnEff(self, task):
        pass
