import pandas as pd
import json
import sys, getopt


class Parser:
    def __init__(self, task):
        self.task = str(task[0])
        self.deadline = int(task[1])
        self.wcet1188 = int(task[2])
        self.wcet918 = int(task[3])
        self.wcet648 = int(task[4])
        self.wcet384 = int(task[5]) 

    def __str__(self):
        return ('Task: {0}  Deadline: {1}  WCET1188: {2}  WCET918: {3}  WCET648: {4}  WCET384: {4}'
                .format(self.task, self.deadline, self.wcet1188, self.wcet918, self.wcet648, self.wcet384))

