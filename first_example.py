from ortools.constraint_solver import pywrapcp
solver = pywrapcp.Solver('First_example')

x = solver.IntVar(0, 2, 'X')
y = solver.IntVar(0, 2, 'Y')
z = solver.IntVar(0, 2, 'Z')

solver.Add(x != y)
# in this case the int_var_default is the lexycographic order
db = solver.Phase([x, y, z], solver.INT_VAR_DEFAULT, solver.INT_VALUE_DEFAULT)

monitors = []
solve = solver.Solve(db, monitors)

count = 0
while solver.NextSolution():
    count += 1
    print("Solution {}: {}".format(count, [x.Value(), y.Value(), z.Value()]))
