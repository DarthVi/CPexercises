from ortools.constraint_solver import pywrapcp
from utils import nqueens_utils as utils
import argparse


def solve_nqueens_ch_1_rc(n):
    solver = pywrapcp.Solver('nqueens_ch_1_rc')

    rows = [solver.IntVar(0, n - 1, str(i)) for i in range(n)]
    columns = [solver.IntVar(0, n - 1, str(i)) for i in range(n)]

    for i in range(n):
        for j in range(n):
            if i < j:
                solver.Add(abs(rows[i] - rows[j]) != abs(i - j))

    # global constraint that does the channeling
    solver.Add(solver.InversePermutationConstraint(rows, columns))

    db = solver.Phase(rows + columns, solver.INT_VAR_DEFAULT, solver.INT_VALUE_DEFAULT)

    monitors = []

    collector = solver.AllSolutionCollector()
    collector.Add(rows)
    collector.Add(columns)

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

    solve_nqueens_ch_1_rc(n)