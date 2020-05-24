from ortools.constraint_solver import pywrapcp
from utils import graph_utils
import os

def gc_model_unsat(instance, avl_colors):
    
    n_nodes, edges = graph_utils.load_instance(instance)
    solver = pywrapcp.Solver('gc_model_unsat')

    nodes = [solver.IntVar(1, avl_colors) for i in range(n_nodes)]
    for i in range(len(edges)):
        solver.Add(nodes[edges[i][0] - 1] != nodes[edges[i][1] - 1])

    monitors = []
	
    collector = solver.FirstSolutionCollector()  # This is a monitor
    collector.Add(nodes)
    monitors.append(collector)

    # impact-based
    parameters = pywrapcp.DefaultPhaseParameters()
    parameters.var_selection_schema = parameters.CHOOSE_MAX_AVERAGE_IMPACT
    parameters.value_selection_schema = parameters.SELECT_MIN_IMPACT

    db = solver.DefaultPhase(nodes, parameters)

    # lexicografic
    # db = solver.Phase(nodes, solver.INT_VAR_DEFAULT, solver.INT_VALUE_DEFAULT)

    # min domain
    # db = solver.Phase(nodes, solver.CHOOSE_MIN_SIZE, solver.INT_VALUE_DEFAULT)

    # random
    # db = solver.Phase(nodes, solver.CHOOSE_RANDOM, solver.INT_VALUE_DEFAULT)
    
    
    max_time = 1000 * 60 * 10  # 10 Minutes
    timelimit = solver.TimeLimit(max_time)  # This is another monitor
    monitors.append(timelimit)
    
    if solver.Solve(db, monitors):
        print('Solved in {} ms. {} branches and {} failures'.format(collector.WallTime(0), collector.Branches(0), collector.Failures(0)))
    else:
        print('Not solved')

if __name__ == '__main__':
    #===========================================================================
    #instance_name, avl_colors = 'fpsol2.i.1.col', 65
    instance_name, avl_colors = 'le450_25a.col', 25
    # instance_name, avl_colors = 'le450_5a.col', 5
    # instance_name, avl_colors = 'david.col', 11
    # instance_name, avl_colors = 'miles250.col', 8
    #===========================================================================

    instance = os.path.join('data/', instance_name)
    assert(os.path.isfile(instance))
    
    gc_model_unsat(instance, avl_colors - 1)
