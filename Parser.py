class Parser:
    def __init__(self, task):
        self.task = str(task[0])
        self.deadline = int(task[1])
        self.wcet1188 = int(task[2])
        self.wcet918 = int(task[3])
        self.wcet648 = int(task[4])
        self.wcet384 = int(task[5]) 

    def __str__(self):
        return ('Task: {0}  Deadline: {1}  WCET1188: {2}  WCET918: {3}  WCET648: {4}  WCET384: {5}'
                .format(self.task, self.deadline, self.wcet1188, self.wcet918, self.wcet648, self.wcet384))

class Header:
    def __init__(self,task):
        self.task = str(task[0])
        self.Exetime = int(task[1])
        self.power1188 = int(task[2])
        self.power918 = int(task[3])
        self.power648 = int(task[4])
        self.power384 = int(task[5]) 
        self.ideal = int(task[6]) 

    def __str__(self):
        return ('Task: {0}  Execution: {1}  Power@1188: {2}  Power@918: {3}  Power@648: {4}  Power@384: {5} Power@IDEL: {6}'
                .format(self.task, self.Exetime, self.power1188, self.power918, self.power648, self.power384, self.ideal))