import pulp as pl
from typing import Dict, List


def build_cvrp(
    nodes: List[int],
    customers: List[int],
    distance: Dict[tuple, float],
    demand: Dict[int, int],
    vehicle_cap: int,
    maximum_vehicles: int,
    emission_factor: float
):
    depot = 0
    model = pl.LpProblem("LastMile CVRP Emissions: ", pl.LpMinimize)

    x = {
        (i, j): pl.LpVariable(f"x_{i}_{j}", 0, 1, cat="Binary")
        for i in nodes for j in nodes if i != j
    }

    f = {
        (i, j): pl.LpVariable(f"f_{i}_{j}", lowBound=0, cat="Continuous")
        for i in nodes for j in nodes if i != j
    }

    model += pl.lpSum(
        emission_factor * distance[(i, j)] * x[(i, j)]
        for (i, j) in x
    )

    for i in customers:
        model += pl.lpSum(x[(i, j)] for j in nodes if j != i) == 1
        model += pl.lpSum(x[(j, i)] for j in nodes if j != i) == 1

    model += pl.lpSum(x[(depot, j)] for j in customers) <= maximum_vehicles
    model += pl.lpSum(x[(i, depot)] for i in customers) <= maximum_vehicles

    demand_total = sum(demand[i] for i in customers)
    model += pl.lpSum(f[(depot, j)] for j in customers) == demand_total

    for i in customers:
        model += (
            pl.lpSum(f[(i, j)] for j in nodes if j != i) -
            pl.lpSum(f[(j, i)] for j in nodes if j != i)
            == demand[i]
        )

    for (i, j) in x:
        model += f[(i, j)] <= vehicle_cap * x[(i, j)]

    return model, x, f