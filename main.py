import pulp as pl

from config import (
    ROUTE_JSON_PATH,
    MAX_CUSTOMERS,
    RANDOM_SEED,
    VEHICLE_CAPACITY,
    MAX_VEHICLES,
    EMISSION_FACTOR
)
from data_loader import load_route_instance
from distance import build_distance_dict
from model import build_cvrp
from solver import extract_routes, compute_metrics


def main():
    
    nodes, customers, coords, demand = load_route_instance(
        ROUTE_JSON_PATH,
        MAX_CUSTOMERS,
        RANDOM_SEED
    )
    distance = build_distance_dict(nodes, coords)

    model, x, f = build_cvrp(
        nodes=nodes,
        customers=customers,
        distance=distance,
        demand=demand,
        vehicle_cap=VEHICLE_CAPACITY,
        maximum_vehicles=MAX_VEHICLES,
        emission_factor=EMISSION_FACTOR
    )

    print("\nSolving optimisation model...")
    solver = pl.PULP_CBC_CMD(msg=True)
    model.solve(solver)
    status = pl.LpStatus[model.status]
    print(f"\nSolver status: {status}")
    if status != "Optimal":
        print("\nModel did not reach optimality. Adjust settings.")
        return
    x_sol = {(i, j): pl.value(var) for (i, j), var in x.items()}
    all_routes = extract_routes(nodes, x_sol)
    summary = compute_metrics(all_routes, distance, EMISSION_FACTOR)
    print("\n=== OPTIMAL all_routes ===")
    for r in summary:
        print(
            f"Route {r['route_id']}: {r['nodes']} | "
            f"{r['distance_km']:.2f} km | {r['emissions_kg']:.2f} kg CO2"
        )

    print("\n=== TOTALS ===")
    print(f"Total Distance: {sum(r['distance_km'] for r in summary):.2f} km")
    print(f"Total Emissions: {sum(r['emissions_kg'] for r in summary):.2f} kg CO2")


if __name__ == "__main__":
    main()