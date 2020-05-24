from os import path
from json import load
from collections import namedtuple
from ortools.constraint_solver import pywrapcp

TaskClass = namedtuple("Task", ['id', 'duration', 'request', 'successors'])

def load_instance(fp):
    """
        @param fp: Filepath of the instance
        @return Capacity, List of Activities (TaskClasses) 
    
    """
    assert(path.exists(fp)), 'The {} file doesn\'t exists.'.format(fp)
    
    instance_data = None
    with open(fp) as fobj:
        instance_data = load(fobj)
    
    print('Loading instance: {}'.format(instance_data['instance']))
    return instance_data['capacity'], [TaskClass(id, t_data['duration'], t_data['request'], t_data['successors']) for id, t_data in instance_data['tasks'].items()]

def print_schedule(intervals, collector):
    print('Best solution: ', collector.ObjectiveValue(0))
    for i in intervals:
        print('Task {} starts at {}'.format(i.Name(), collector.Solution(0).StartValue(i)))

class PRB_MinStartTime(pywrapcp.PyDecisionBuilder):
    def __init__(self, vars):
        pywrapcp.PyDecisionBuilder.__init__(self)
        self.__vars = vars
    
    def Next(self, solver):
        for var in self.__vars:
            var.SetStartMax(var.StartMin()) 
        return None