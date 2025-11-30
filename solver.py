from typing import Dict, List


def extract_routes(nodes, x_sol):
    depot = 0
    active_arcs = {(i, j) for (i, j), v in x_sol.items() if v > 0.5}
    all_routes = []

    while True:
        start = [(i, j) for (i, j) in active_arcs if i == depot]
        if not start:
            break

        _, next = start[0]
        route = [depot, next]
        active_arcs.remove((depot, next))
        current_node = next

        while current_node != depot:
            outgoing = [(i, j) for (i, j) in active_arcs if i == current_node]
            if not outgoing:
                break
            _, next = outgoing[0]
            route.append(next)
            active_arcs.remove((current_node, next))
            current_node = next

        all_routes.append(route)

    return all_routes


def compute_metrics(all_routes, dist, emission_factor):
    summary = []
    for idx, route in enumerate(all_routes, start=1):
        distance = sum(dist[(i, j)] for i, j in zip(route[:-1], route[1:]))
        co2 = emission_factor * distance
        summary.append({
            "route_id": idx,
            "nodes": route,
            "distance_km": distance,
            "emissions_kg": co2
        })
    return summary