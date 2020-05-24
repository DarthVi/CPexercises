def print_magic_square(flatboard, n, collector, solutions=None):
    """
    Prints the magic square board
    :param flatboard: A list of variable which represents the board
    :param n: The number of rows and columns of the board (n x n)
    :param collector: A solution collector
    :param solutions: None show all solutions stored in the collector.
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
        board = ''
        for r in range(n*n):
            board += "|" + collector.Solution(i).Value(r) + "|"
            #if r == k*n with k from 1 to n
            if r % n == 0:
                board += "\n"
        print(board)
        print()