import random
import collections


class Edge:
    """
    Represents an edge in a graph.

    Attributes:
        u: The source vertex of the edge.
        v: The destination vertex of the edge.
        weight: The weight of the edge.
    """

    u = ()
    v = ()
    weight = 0

    def __init__(self, u, v, weight):
        """
        Appends a vertex to the list of vertices.

        Args:
            u: The starting vertex.
            t: The timestamp of the vertex.
        """
        self.u = u
        self.v = v
        self.weight = weight


def buildGraph(P):
    """
    Builds a graph based on a list of input data.

    Args:
        P: A list of input data, where each element is a tuple containing u, v, t, and l.

    Returns:
        A tuple containing the list of vertices and the list of edges.
    """

    edges = []
    vertices = []

    for i in P:
        u, v, t, l = i

        if (u, t) not in vertices:
            vertices.append((u, t))

        if (v, t + l) not in vertices:
            vertices.append((v, t + l))

        edge = Edge((u, t), (v, t + l), l)

        edges.append(edge)

    clustered_vertices = collections.defaultdict(list)

    for e in vertices:
        clustered_vertices[e[0]].append(e)

    for i, value in clustered_vertices.items():
        edges.extend(
            Edge(clustered_vertices[i][j], clustered_vertices[i][j + 1], 0)
            for j in range(len(value) - 1)
        )

    return vertices, edges


def generate_graph_G(nb_vertices, nb_edges):
    """
    Generates a graph G with the specified number of vertices and edges.

    Args:
        nb_vertices (int): The number of vertices in the graph.
        nb_edges (int): The number of edges in the graph.

    Returns:
        list: A list of edges representing the generated graph.

    """

    G = []
    last_node = nb_vertices - 1

    for i in range(nb_edges):
        starting_node = i % last_node
        end_node = random.randint(
            starting_node, starting_node + (starting_node + 5) % (last_node + 1)
        )

        departure_date = random.randint(1, 14)

        edge = (f"s{starting_node}", f"s{end_node}", departure_date, 1)

        G.append(edge)

    return G
