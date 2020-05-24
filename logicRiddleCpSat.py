from ortools.constraint_solver import pywrapcp
from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s = %i' % (v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count

if __name__ == '__main__':

    model = cp_model.CpModel()

    a = model.NewBoolVar('A') # All of the below
    b = model.NewBoolVar('B') # None of the below
    c = model.NewBoolVar('C') # All of the above
    d = model.NewBoolVar('D') # One of the above
    e = model.NewBoolVar('E') # None of the above
    f = model.NewBoolVar('F') # None of the above

    # model.Add(a != False).OnlyEnforceIf(b and c and d and e and f )
    # model.Add(b != False).OnlyEnforceIf(b.Not() and c.Not() and d.Not() and e.Not() and f.Not())
    # model.Add(c != False).OnlyEnforceIf(a and b )
    # model.Add(d != False).OnlyEnforceIf(a or b or c )
    # model.Add(e != False).OnlyEnforceIf(a.Not() and b.Not() and c.Not() and d.Not())
    # model.Add(f != False).OnlyEnforceIf(a.Not() and b.Not() and c.Not() and d.Not() and e.Not())

    model.Add(b == True and c == True and d == True and e == True and f == True).OnlyEnforceIf(a.Not())
    model.Add(b == False and c == False and d == False and e == False and f == False).OnlyEnforceIf(b.Not())
    model.Add(a == True and b == True).OnlyEnforceIf(c.Not())
    model.Add(a == True or b == True or c == True).OnlyEnforceIf(d.Not())
    model.Add(a == False and b == False and c == False and d == False).OnlyEnforceIf(e.Not())
    model.Add(a == False and b == False and c == False and d == False and e == False).OnlyEnforceIf(f.Not())
    
    # Create a solver and solve.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([a, b, c, d, e, f])
    status = solver.SearchForAllSolutions(model, solution_printer)

    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: %i' % solution_printer.solution_count())
