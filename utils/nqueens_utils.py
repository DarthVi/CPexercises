def print_boards(rows, collector, solutions=None):
    """
        @param rows: A list of variables which represents the board.
        @param collector: A solution collector
        @param solutions: None show all solutions stored in the collector. 
            A list of the indexes to show [0, n-1]. Will show the first and the last solution stored in the collector. 
            n corresponds to collector.SolutionCount() 
          
    """    
    if not solutions:
        solutions = range(collector.SolutionCount())

    assert(isinstance(solutions, (tuple, list, range))), 'Only list, tuple or range are accepted'

    for i in solutions:
        if i >= collector.SolutionCount():
            continue
        print('Solution #{}'.format(i + 1))
        print('- Walltime {} ms'.format(collector.WallTime(i)))
        print('- Branches {}'.format(collector.Branches(i)))
        print('- Failures {}'.format(collector.Failures(i)))
        n = len(rows)
        for r in rows:
            row_line = ''
            for j in range(n):
                if collector.Solution(i).Value(r) == j:
                    row_line += 'Q '
                else:
                    row_line += '- '
            
            print(row_line)
        
        print()
