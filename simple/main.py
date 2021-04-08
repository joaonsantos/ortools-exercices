from ortools.sat.python import cp_model
"""
Let's start with a simple example problem in which there are:

    Three variables, x, y, and z, each of which can take on the values: 0, 1, or 2.
    One constraint: x ≠ y
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


def cp_program():
    # creates the model
    model = cp_model.CpModel()

    # initialize the domain

    domain = {
        "x": model.NewIntVar(0, 2, 'x'),
        "y": model.NewIntVar(0, 2, 'y'),
        "z": model.NewIntVar(0, 2, 'z')
    }

    # add a constraint
    model.Add(domain['x'] != domain['y'])
    model.AddAllDifferent([var for _,var in domain.items()])

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
    cp_program()
