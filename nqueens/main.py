from ortools.sat.python import cp_model
"""
Let's start with a simple example problem in which there are:

    Three variables, x, y, and z, each of which can take on the values: 0, 1, or 2.
    constraints: x ≠ y ≠ z.
"""

def print_solution(solver, status, domain, all_states, accepted_states):
    print(f'#=== Possible states ===#\n')
    for name, value in all_states.items():
        print(f'{name} = {value}')


    print(f'#=== Solver ===#\n')
    print(f'status = {status}')
    if status in accepted_states:
        for name, var in domain.items():
            print(f'{name} = {solver.Value(var)}')


def cp_nqueens(num_queens):
    # creates the model
    model = cp_model.CpModel()

    # initialize the domain
    domain = {}


    # assuming queen(i) is positioned on row i, column is now the unknown
    for i in range(num_queens):
        var_name = "q" + str(i)
        domain[var_name] = model.NewIntVar(0, num_queens - 1, var_name)


    # add constraints
    for i in range(num_queens):
        for j in range(num_queens):
            if i == j:
                continue

            # all columns must be different
            var1_name = "q" + str(i)
            var2_name = "q" + str(j)
            model.Add(domain[var1_name] != domain[var2_name])


            # queens must not be diagonal to each other
            offset = j - i
            model.Add(domain[var1_name] != (domain[var2_name] + offset))
            model.Add(domain[var1_name] != (domain[var2_name] - offset))

    # create a solver and apply it to the model defined earlier
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    all_states = {
        "unknown": cp_model.UNKNOWN,
        "invalid": cp_model.MODEL_INVALID,
        "feasible": cp_model.FEASIBLE,
        "infeasible": cp_model.INFEASIBLE,
        "optimal": cp_model.OPTIMAL
    }
    accepted_states = [cp_model.OPTIMAL, cp_model.FEASIBLE]
    print_solution(solver, status, domain,  all_states, accepted_states)

if __name__ == "__main__":
    cp_nqueens(4)
