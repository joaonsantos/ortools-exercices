from ortools.sat.python import cp_model
import traceback
import sys
"""
In recreational mathematics, a square array of numbers is said to be a magic
square if the sums of the numbers in each row, each column, and both main
diagonals are the same. Each entry in the square must be different to not be
trivial. The order of the magic square is the number of integers along one
side. A magic square is said to be normal if the array includes just the
positive integers 1..n^2.

-> How to solve a magic square of order n?
"""


def print_solution(solver, status, domain, order, accepted_states):
    print('solution:')
    if status in accepted_states:
        for i in range(order):
            for j in range(order):
                var_name = "n%s%s" % (str(i), str(j))
                print('%2s' % solver.Value(domain[var_name]), end=" ")
            print('')

    print('')
    print(f'stats:')
    print('  - status          : %s' % solver.StatusName(status))
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())


def cp_msquare(order):
    # creates the model
    model = cp_model.CpModel()

    # initialize the domain
    domain = {}

    # define variables and domains
    for i in range(order):
        for j in range(order):
            var_name = "n%s%s" % (str(i), str(j))
            domain[var_name] = model.NewIntVar(1, order * order, var_name)

    # all entries must be different
    model.AddAllDifferent([var for _, var in domain.items()])

    # create list of line variable sums
    line_sum_vars = []
    line_sum_var_names = []
    for i in range(order):
        line_vars = []
        line_var_names = []
        for j in range(order):
            var_name = "n%s%s" % (str(i), str(j))
            line_vars.append(domain[var_name])
            line_var_names.append(var_name)

        line_sum_vars.append(sum(line_vars))
        line_sum_var_names.append([line_var_names])

    # debug
    # print(f'line constraints {line_constraints_names}')

    # create list of column variable sums
    column_sum_vars = []
    column_sum_names = []
    for j in range(order):
        column_vars = []
        column_var_names = []
        for i in range(order):
            var_name = "n%s%s" % (str(i), str(j))
            column_vars.append(domain[var_name])
            column_var_names.append(var_name)

        column_sum_vars.append(sum(column_vars))
        column_sum_names.append([column_var_names])

    # debug
    # print(f'column constraints: {column_constraints_names}')

    # sum must also be the same as the column and line sum in the main diagonals
    main_diagonal_vars = []
    main_diagonal_vars_names = []

    anti_diagonal_vars = []
    anti_diagonal_vars_names = []
    for i in range(order):
        for j in range(order):
            if i == j:
                var_name = "n%s%s" % (str(i), str(j))
                main_diagonal_vars.append(domain[var_name])
                main_diagonal_vars_names.append(var_name)

            if j == ((order-1) - i):
                var_name = "n%s%s" % (str(i), str(j))
                anti_diagonal_vars.append(domain[var_name])
                anti_diagonal_vars_names.append(var_name)


    main_diagonal_sum = sum(main_diagonal_vars)
    anti_diagonal_sum = sum(anti_diagonal_vars)

    # enforce equality among all lines and equality among all columns
    # as well as equality among all lines and columns and main diagonals
    for i in range(order):
        for j in range(order):
            model.Add(column_sum_vars[i] == column_sum_vars[j])
            model.Add(line_sum_vars[i] == line_sum_vars[j])
            model.Add(line_sum_vars[i] == column_sum_vars[j] == main_diagonal_sum == anti_diagonal_sum)

    # create a solver and apply it to the model defined earlier
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    accepted_states = [cp_model.OPTIMAL, cp_model.FEASIBLE]
    print_solution(solver, status, domain, order, accepted_states)


if __name__ == "__main__":
    try:
        order = int(sys.argv[1])
        cp_msquare(order)
    except Exception as e:
        traceback.print_exc()
        print(
            "usage: python main.py <o>, in which o is the order of the normal magic square"
        )
        sys.exit(1)
