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

    # create list of column variable sums
    column_constraints = []
    column_constraints_names = []
    for i in range(order):
        column_vars = []
        column_vars_names = []
        for j in range(order):
            var_name = "n%s%s" % (str(i), str(j))
            column_vars.append(domain[var_name])
            column_vars_names.append(var_name)

        column_constraints.append(sum(column_vars))
        column_constraints_names.append([column_vars_names])

    # debug
    # print(f'column constraints {column_constraints_names}')

    # create list of line variable sums
    line_constraints = []
    line_constraints_names = []
    for j in range(order):
        line_vars = []
        line_vars_names = []
        for i in range(order):
            var_name = "n%s%s" % (str(i), str(j))
            line_vars.append(domain[var_name])
            line_vars_names.append(var_name)

        line_constraints.append(sum(line_vars))
        line_constraints_names.append([line_vars_names])

    # debug
    # print(f'line constraints: {line_constraints_names}')

    # enforce equality among all lines and equality among all columns
    # as well as equality among all lines and columns
    for i in range(order):
        for j in range(order):
            model.Add(column_constraints[i] == column_constraints[j])
            model.Add(line_constraints[i] == line_constraints[j])
            model.Add(line_constraints[i] == column_constraints[j])

    # TODO sum must also be the same as the column and line sum in the main diagonals

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
