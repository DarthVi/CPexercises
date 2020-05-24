from ortools.constraint_solver import pywrapcp

if __name__ == '__main__':
    solver = pywrapcp.Solver('logic_riddle')

    a = solver.IntVar(0, 1, 'A')  # All of the below
    b = solver.IntVar(0, 1, 'B')  # None of the below
    c = solver.IntVar(0, 1, 'C')  # All of the above
    d = solver.IntVar(0, 1, 'D')  # One of the above
    e = solver.IntVar(0, 1, 'E')  # None of the above
    f = solver.IntVar(0, 1, 'F')  # None of the above

    solver.Add(a == 1 and b == 1 and c == 1 and d == 1 and e == 1 and f == 1)
    solver.Add(b == 1 and b == 0 and c == 0 and d == 0 and e == 0 and f == 0)
    solver.Add(c == 1 and a == 1 and b == 1)
    solver.Add(d == 1 and (a == 1 or b == 1 or c == 1))
    solver.Add(e == 1 and a == 0 and b == 0 and c == 0 and d == 0)
    solver.Add(f == 1 and a == 0 and b == 0 and c == 0 and d == 0 and e == 0)

    # in this case the int_var_default is the lexycographic order
    db = solver.Phase([a, b, c, d, e, f], solver.INT_VAR_DEFAULT, solver.INT_VALUE_DEFAULT)

    vars = [a, b, c, d, e, f]
    solution = solver.AllSolutionCollector()
    solution.Add(vars)

    solved = solver.Solve(db, [solution])
    if solved:
        for i in range(solution.SolutionCount()):
            print(["{} - {}: {}".format(i + 1, v.Name(), solution.Value(i, v)) for v in vars])