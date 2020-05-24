from ortools.constraint_solver import pywrapcp
from utils import magic_square_utils as utils
def magic_square(n, var_selection_schema, value_selection_schema, luby_restart_frequency=None):
    max_number = n * n
    
    solver = pywrapcp.Solver('magic_square')

    board = []
    flat_board = []
    for i in range(n):
        board.append([])
        for j in range(n):
            var = solver.IntVar(1, max_number, 'x_{}{}'.format(i, j))
            board[i].append(var)
            flat_board.append(var)

    sum = solver.IntVar(1, max_number * (1 + max_number) // 2)
    solver.Add(solver.AllDifferent(flat_board))

    for i in range(n):
        solver.Add(solver.Sum([board[i][j] for j in range(n)]) == sum)
        solver.Add(solver.Sum([board[j][i] for j in range(n)]) == sum)

    solver.Add(solver.Sum([board[i][i] for i in range(n)]) == sum)
    solver.Add(solver.Sum([board[i][n - i - 1] for i in range(n)]) == sum)

    monitors = []
        
    parameters = pywrapcp.DefaultPhaseParameters()
    parameters.var_selection_schema = getattr(parameters, var_selection_schema)
    parameters.value_selection_schema = getattr(parameters, value_selection_schema)

    db = solver.DefaultPhase(flat_board, parameters)
    
    collector = solver.FirstSolutionCollector()
    collector.Add(flat_board)
    collector.Add(sum)  
    monitors.append(collector)
       
    max_time = 1000 * 60 * 10
    timelimit = solver.TimeLimit(max_time)
    monitors.append(timelimit)

    if luby_restart_frequency:
        monitors.append(solver.LubyRestart(luby_restart_freq))
    
    if solver.Solve(db, monitors):
        print('Solved in {} ms. {} branches and {} failures'.format(collector.WallTime(0), collector.Branches(0), collector.Failures(0)))
        count = 0
        while solver.NextSolution():
            count +=1
            board = ''
            for r in range(n * n):
                board += "|" + str(flat_board[r].Value()) + "|"
                # if r == k*n with k from 1 to n
                if (r+1) % n == 0:
                    board += "\n"
            print(board)
            print()
        #utils.print_magic_square(flat_board, n, collector)
    else:
        print('Time out')
                
if __name__ == '__main__':
    #===========================================================================
    # n = 5
    # n = 6
    n = 3
    #===========================================================================
    
    #===========================================================================
    # var_selection_schema = 'CHOOSE_MAX_SUM_IMPACT'
    # var_selection_schema = 'CHOOSE_MAX_AVERAGE_IMPACT'
    var_selection_schema = 'CHOOSE_MAX_VALUE_IMPACT'
    #===========================================================================
    
    #===========================================================================
    # value_selection_schema = 'SELECT_MIN_IMPACT'
    value_selection_schema = 'SELECT_MAX_IMPACT'
    #===========================================================================
    
    #===========================================================================
    #luby_restart_freq = None
    luby_restart_freq = 200
    #===========================================================================
    
    magic_square(n, var_selection_schema, value_selection_schema, luby_restart_frequency=luby_restart_freq)

