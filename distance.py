import math
from typing import Dict, List


def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2)**2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2)

    return 2 * R * math.asin(math.sqrt(a))


def build_distance_dict(nodes: List[int], coords: Dict[int, tuple]):
    distance = {}
    for i in nodes:
        lat1, lon1 = coords[i]
        for j in nodes:
            if i == j:
                continue
            lat2, lon2 = coords[j]
            distance[(i, j)] = haversine(lat1, lon1, lat2, lon2)
    return distance