from ortools.constraint_solver import pywrapcp

solver = pywrapcp.Solver('first try')

x = solver.IntVar(0, 2, 'X')
z = solver.IntVar(0, 2, 'Z')

values = [0, 1, 2]

y = solver.IntVar(values, 'Y')

print(x != y)
solver.Add(x != y)

vars = [x, y,  z]

print(x + 2)
print(y)

# here there's what to do to search for the first solution
solution = solver.FirstSolutionCollector()

#if we want all solutions in the monitor
# solution = solver.AllSolutionCollector()
solution.Add(vars)

db = solver.Phase(vars, solver.INT_VAR_DEFAULT, solver.INT_VALUE_DEFAULT)

solved = solver.Solve(db, [solution])

if solved:
    for v in vars:
        print(v.Name(), solution.Value(0, v))

solution = solver.AllSolutionCollector()
solution.Add(vars)

alldiff = solver.AllDifferent(vars)
print(alldiff)
solver.Add(alldiff)

solved = solver.Solve(db, [solution])
if solved:
    for i in range(solution.SolutionCount()):
        print(["{} - {}: {}".format(i + 1, v.Name(), solution.Value(i, v)) for v in vars])

