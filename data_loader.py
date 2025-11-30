import json
import random
from pathlib import Path
from typing import Tuple, Dict, List


def load_route_instance(
    path_json: Path,
    max_customers: int,
    seed: int
) -> Tuple[List[int], List[int], Dict[int, tuple], Dict[int, int]]:
    """
    Load the dataset and convert ONE route into:
    - nodes (with depot=0)
    - customers (1..n)
    - coords {id: (lat, lng)}
    - demand {id: demand units}
    """

    print(f"Loading route data from: {path_json.resolve()}")

    with open(path_json, "r") as f:
        data = json.load(f)
    route_sizes = []
    for rid, route in data.items():
        stops_obj = route["stops"]
        if isinstance(stops_obj, dict):
            n_stops = len(stops_obj)
        else: 
            n_stops = len(stops_obj)
        route_sizes.append((rid, n_stops))
    candidates = [(rid, s) for rid, s in route_sizes if 20 <= s <= 40]
    if not candidates:
        raise ValueError("No route found with 20–40 stops.")

    chosen_route_id, stop_count = candidates[0]
    print(f"Chosen route: {chosen_route_id} with {stop_count} stops.")

    stops_obj = data[chosen_route_id]["stops"]

    stops_list = []

    if isinstance(stops_obj, dict):
        for key, stop in stops_obj.items():
            stop = dict(stop)  # copy
            if "sequence" in stop:
                seq = int(stop["sequence"])
            else:
                try:
                    seq = int(key)
                except ValueError:
                    seq = len(stops_list)
            stop["sequence"] = seq
            stops_list.append(stop)
    else:
        for idx, stop in enumerate(stops_obj):
            stop = dict(stop)
            if "sequence" in stop:
                seq = int(stop["sequence"])
            else:
                seq = idx
            stop["sequence"] = seq
            stops_list.append(stop)

    stops_list.sort(key=lambda s: int(s["sequence"]))
    
    if len(stops_list) > max_customers:
        stops_list = stops_list[:max_customers]
        print(f"Truncated to first {max_customers} stops.")

    coords: Dict[int, tuple] = {}
    demand: Dict[int, int] = {}
    random.seed(seed)

    for s in stops_list:
        seq = int(s["sequence"])
        lat = float(s["lat"])
        lng = float(s["lng"])
        stype = str(s.get("type", "")).lower()

        if seq == 0 or stype == "depot":
            node_id = 0
            dem = 0
        else:
            node_id = seq
            dem = random.randint(1, 5) 

        coords[node_id] = (lat, lng)
        demand[node_id] = dem

    nodes = sorted(coords.keys())
    customers = [i for i in nodes if i != 0]

    print(f"Instance created: depot + {len(customers)} customers.")
    return nodes, customers, coords, demand