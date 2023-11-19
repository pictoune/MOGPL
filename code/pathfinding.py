import numpy as np
import collections


def bellman_ford(vertices, edges, start, end):
    """
    Bellman-Ford algorithm for finding the shortest path in a graph.

    Args:
        vertices (list): List of vertices in the graph.
        edges (list): List of edges in the graph.
        start: The starting vertex.
        end: The target vertex.

    Returns:
        tuple: A tuple containing the distance of the shortest path and the path itself.
    """
    distances = {v: float("inf") for v in vertices}
    distances[start] = 0
    parents = collections.defaultdict(lambda: None)

    for _ in range(len(vertices) - 1):
        for edge in edges:
            if distances[edge.u] + edge.weight < distances[edge.v]:
                distances[edge.v] = distances[edge.u] + edge.weight
                parents[edge.v] = edge.u

    distance = distances[end]

    if end in parents:
        path = []
        parent = end

        while parent:
            path.append(parent)
            parent = parents[parent]
        path.reverse()

        return distance, path
    else:
        print("No path found")

        return float("inf"), []


def dijkstra(vertices, edges, start, end):
    """Apply Dijkstra's algorithm to find the shortest path between two vertices.

    Args:
        vertices (list): List of vertices in the graph.
        edges (list): List of edges in the graph.
        start: The starting vertex.
        end: The target vertex.

    Returns:
        tuple: A tuple containing the shortest distance and the path as a list of vertices.
    """
    nodes = {
        vertex: {"distance": np.inf, "visited": False, "predecessor": None}
        for vertex in vertices
    }
    nodes[start].update({"distance": 0, "predecessor": None})

    for _ in vertices:
        selected_node = min(
            (node for node in nodes if not nodes[node]["visited"]),
            key=lambda node: nodes[node]["distance"],
            default=None,
        )

        if selected_node is None:
            break

        nodes[selected_node]["visited"] = True

        # Update distances for unvisited neighbors
        for edge in edges:
            if selected_node == edge.u and not nodes[edge.v]["visited"]:
                neighbor = edge.v
                new_distance = nodes[edge.u]["distance"] + edge.weight
                if nodes[neighbor]["distance"] > new_distance:
                    nodes[neighbor].update(
                        {"distance": new_distance, "predecessor": edge.u}
                    )

    # Construct path if it exists
    if nodes[end]["distance"] != np.inf:
        path = []
        current = end
        while current != start:
            path.insert(0, current)
            current = nodes[current]["predecessor"]
        path.insert(0, start)

        return nodes[end]["distance"], path
    else:
        print("No path found")

        return float("inf"), []


def type_1(vertices, edges, start, end):
    """Find a path in a graph from a start vertex to an end vertex using the type 1 algorithm.

    Args:
        vertices (list): List of vertices in the graph.
        edges (list): List of edges in the graph.
        start: The starting vertex.
        end: The target vertex.

    Returns:
        list or None: A list of edges representing the path from the start vertex to the end vertex,
            or None if no path is found.
    """
    clustered_vertices = collections.defaultdict(list)

    for vertex in vertices:
        clustered_vertices[vertex[0]].append(vertex)

    source = min(clustered_vertices[start], key=lambda k: k[1])
    destinations = sorted(clustered_vertices[end], key=lambda k: k[1])

    for destination in destinations:
        _, path = bellman_ford(vertices, edges, source, destination)
        if path != {}:
            return [
                (path[vertex][0], path[vertex + 1][0], path[vertex][1], 1)
                for vertex in range(len(path) - 1)
                if path[vertex][0] != path[vertex + 1][0]
            ]

    return None


def type_2(vertices, edges, start, end):
    """Find a path in a graph from a start vertex to an end vertex using the type 2 algorithm.

    Args:
        vertices (list): List of vertices in the graph.
        edges (list): List of edges in the graph.
        start: The starting vertex.
        end: The target vertex.

    Returns:
        list or None: A list of edges representing the path from the start vertex to the end vertex,
            or None if no path is found.
    """
    clustered_vertices = collections.defaultdict(list)

    for vertex in vertices:
        clustered_vertices[vertex[0]].append(vertex)

    sources = sorted(clustered_vertices[start], key=lambda k: k[1], reverse=True)
    destination = max(clustered_vertices[end], key=lambda k: k[1])

    for source in sources:
        _, path = bellman_ford(vertices, edges, source, destination)
        if path:
            return [
                (path[i][0], path[i + 1][0], path[i][1], 1)
                for i in range(len(path) - 1)
                if path[i][0] != path[i + 1][0]
            ]

    return None


def type_3(vertices, edges, start, end):
    """Find a path in a graph from a start vertex to an end vertex using the type 3 algorithm.

    Args:
        vertices (List[Tuple]): List of vertices.
        edges (List[Tuple]): List of edges.
        start (Any): Start vertex.
        end (Any): End vertex.

    Returns:
        List[Tuple]: List of tuples representing the path.
    """
    clustered_vertices = collections.defaultdict(list)

    for vertex in vertices:
        clustered_vertices[vertex[0]].append(vertex)

    sources = clustered_vertices[start]
    destinations = clustered_vertices[end]
    dictemps = collections.defaultdict(list)

    for source in sources:
        for destination in destinations:
            _, t1 = source
            _, t2 = destination

            if t2 > t1:
                dictemps[t2 - t1].append((source, destination))

    tri = sorted(dictemps.items(), key=lambda k: k[0])

    for _, possible_paths in tri:
        for source, destination in possible_paths:
            _, path = bellman_ford(vertices, edges, source, destination)
            if path:
                return [
                    (u[0], v[0], u[1], 1)
                    for u, v in zip(path, path[1:])
                    if u[0] != v[0]
                ]

    return None


def type_4(e, a, s, d):
    """Find a path in a graph from a start vertex to an end vertex using the type 4 algorithm.

    Args:
        e (List[Tuple]): List of vertices.
        a (Any): Placeholder argument.
        s (Any): Start vertex.
        d (Any): End vertex.

    Returns:
        Tuple: Tuple containing the distance and path.
    """
    clustered_vertices = {i[0]: i for i in e}

    dis, path = bellman_ford(e, a, clustered_vertices[s], clustered_vertices[d])

    path_in_G = []

    for vertex in range(len(path) - 1):
        if path[vertex][0] != path[vertex + 1][0]:
            edge = (path[vertex][0], path[vertex + 1][0], path[vertex][1], 1)
            path_in_G.append(edge)

    return path_in_G, dis
