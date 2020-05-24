from ortools.constraint_solver import pywrapcp 
import argparse
from utils import nqueens_utils as utils


def solve_nqueens_model_1(n):
    
    solver = pywrapcp.Solver('nqueens_model_1')

    rows = [solver.IntVar(0, n - 1, str(i)) for i in range(n)]

    solver.Add(solver.AllDifferent(rows))

    for i in range(n):
        for j in range(n):
            if i < j:
                solver.Add(abs(rows[i] - rows[j]) != abs(i - j))

    db = solver.Phase(rows, solver.INT_VAR_DEFAULT, solver.INT_VALUE_DEFAULT)
    
    monitors = []
    
    collector = solver.AllSolutionCollector()
    collector.Add(rows)
    
    monitors.append(collector)
    
    if solver.Solve(db, monitors):
        utils.print_boards(rows, collector)
    else:
        print('Not solved')
                        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--n', type=int, help='Board size', default=8)
    
    args = parser.parse_args()
    n = args.n
    
    solve_nqueens_model_1(n)