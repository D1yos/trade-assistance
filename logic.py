import math
import heapq


def clean_num(value):
    try:
        if value is None: return None
        return float(str(value).replace(",", ".").strip())
    except (ValueError, AttributeError):
        return None


def find_best_route(data, start_node, end_node):
    if not start_node or not end_node:
        return "Please enter both items."

    graph = {}
    nodes = set()
    for f, t, n, x in data:
        try:
            n, x = float(n), float(x)
            if n <= 0 or x <= 0: continue
            rate = x / n
            nodes.update([f, t])
            if f not in graph: graph[f] = {}
            weight = -math.log(rate)
            if t not in graph[f] or weight < graph[f][t]:
                graph[f][t] = weight
        except (ValueError, ZeroDivisionError):
            continue

    if start_node not in nodes or end_node not in nodes:
        return "No data for selected items."

    queue = [(0, start_node, [])]
    visited = set()
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0

    best_path = None

    while queue:
        (dist, current_node, path) = heapq.heappop(queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        path = path + [current_node]

        if current_node == end_node:
            best_path = path
            break

        for neighbor, weight in graph.get(current_node, {}).items():
            if neighbor not in visited:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(queue, (new_dist, neighbor, path))

    if not best_path:
        return f"No route found from {start_node} to {end_node}."

    total_multiplier = 1.0
    steps_desc = []
    for i in range(len(best_path) - 1):
        u, v = best_path[i], best_path[i + 1]
        best_step_rate = 0
        for f, t, n, x in data:
            if f == u and t == v:
                rate = x / n
                if rate > best_step_rate: best_step_rate = rate

        total_multiplier *= best_step_rate
        steps_desc.append(f"{u} -> {v} (x{round(best_step_rate, 4)})")

    res = f"BEST ROUTE: {' -> '.join(best_path)}\n"
    res += f"TOTAL RATE: 1 {start_node} = {round(total_multiplier, 6)} {end_node}\n"
    if total_multiplier != 0:
        res += f"INVERSE: 1 {end_node} = {round(1 / total_multiplier, 2)} {start_node}\n"
    res += "-" * 30 + "\n" + "\n".join(steps_desc)
    return res