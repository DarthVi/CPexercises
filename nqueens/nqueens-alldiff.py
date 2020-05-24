from ortools.constraint_solver import pywrapcp
from utils import nqueens_utils as utils
import argparse

def solve_nqueen_model_alldiff(n):
    
    solver = pywrapcp.Solver('model_alldiff')

    board = [solver.IntVar(0, n - 1, str(i)) for i in range(n)]
    solver.Add(solver.AllDifferent(board))
    solver.Add(solver.AllDifferent([board[i] + i for i in range(n)]))
    solver.Add(solver.AllDifferent([board[i] - i for i in range(n)]))

    monitors = []

    db = solver.Phase(board, solver.INT_VAR_DEFAULT, solver.INT_VALUE_DEFAULT)

    collector = solver.AllSolutionCollector()
    collector.Add(board)
    
    monitors.append(collector)
    
    if solver.Solve(db, monitors):
        utils.print_boards(board, collector)
    else:
        print('Not solved')
                        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--n', type=int, help='Board size', default=8)
    
    args = parser.parse_args()
    n = args.n
    
    solve_nqueen_model_alldiff(n) 