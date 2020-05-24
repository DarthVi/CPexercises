from utils import rcsp_utils as utils
from ortools.constraint_solver import pywrapcp


def rcpsp(filepath):
    capacity, tasks = utils.load_instance(filepath)
    
    solver = pywrapcp.Solver('RCPSP')

    maxMakespan = sum([i.duration for i in tasks])

    intervals = []

    for i,j in zip(tasks, range(0,len(tasks))):
        interval = solver.FixedDurationIntervalVar(0, maxMakespan, i.duration, False, str(i.id))
        intervals.append(interval)

    for i in tasks:
        for j in i.successors:
            solver.Add(intervals[j].StartsAfterEnd(intervals[int(i.id)]))

    solver.Add(solver.Cumulative(intervals, [task.request for task in tasks], capacity, 'Capacity'))

    obj_func = solver.Minimize(solver.Max([i.EndExpr() for i in intervals]), 1)

    db = solver.Phase(intervals, solver.INTERVAL_SET_TIMES_FORWARD)  # Complete search
    #db = utils.PRB_MinStartTime(intervals)
    collector = solver.BestValueSolutionCollector(False)
    collector.AddObjective(obj_func.Var())

    monitors = []

    monitors.append(obj_func)
        
    collector = solver.BestValueSolutionCollector(False)
    collector.AddObjective(obj_func.Var())
    collector.Add(intervals)
    monitors.append(collector)
    
    if solver.Solve(db, monitors):
        utils.print_schedule(intervals, collector)
    else:
        print('Not solved')
        
if __name__ == '__main__':
    #===========================================================================
    # filepath = 'data/instance1.json'
    # filepath = 'data/instance2.json'
    # filepath = 'data/instance3.json'
    # filepath = 'data/instance4.json'
    filepath = 'data/instance5.json'
    #===========================================================================
    rcpsp(filepath)
