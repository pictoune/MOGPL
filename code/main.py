"""
This module implements various graph-based algorithms and utility functions for solving shortest path problems in a directed graph. It includes implementations of Bellman-Ford and Dijkstra's algorithms, as well as specialized pathfinding methods for different types of paths such as earliest arrival, latest departure, shortest duration, and smallest distance.

Classes:
    Edge: Represents an edge in a graph with a source, destination, and weight.

Functions:
    bellman_ford(vertices, edges, start, end): Implements the Bellman-Ford algorithm to find the shortest path from start to end.
    dijkstra(vertices, edges, start, end): Implements Dijkstra's algorithm to find the shortest path from start to end.
    buildGraph(P): Constructs a graph from a given set of edges.
    type_1(vertices, edges, start, end): Finds the type I path (earliest arrival) in the graph.
    type_2(vertices, edges, start, end): Finds the type II path (departure at the latest) in the graph.
    type_3(vertices, edges, start, end): Finds the type III path (shortest duration) in the graph.
    type_4(vertices, edges, start, end): Finds the type IV path (smallest distance) in the graph.
    readTerminal(): Reads a path specification from the terminal.
    readFile(name): Reads a graph specification from a file.
    gurobi(vertices, edges, start, end): Solves the shortest path problem using the Gurobi optimizer.

The module also includes functions for generating random graphs and analyzing the execution time of algorithms based on the number of vertices and edges.

Authors: Xinan SHAO & Victor PIRIOU
"""
import graph
import pathfinding
import gurobi_solver
import utils


P1 = utils.readFile("code/data.txt")
print(f"Path obtained from the file: {P1}")

V, E = graph.buildGraph(P1)
print(f"\nVertices of G tilde: {V}")
print("Edges of G tilde:")

for edge in E:
    print(
        f"{edge.u[0]},{edge.u[1]} => {edge.v[0]},{edge.v[1]} | weight = {edge.weight}"
    )

start = ("a", 1)
end = ("g", 8)
pathfinding.dijkstra(V, E, start, end)

path_1 = pathfinding.type_1(V, E, "a", "c")
print(f"\ntype I path (earliest arrival) between a and c: {path_1}")

path_2 = pathfinding.type_2(V, E, "a", "g")
print(f"type II path (departure at the latest) between a and g: {path_2}")

path_3 = pathfinding.type_3(V, E, "a", "g")
print(f"type III path (shortest duration) between a and g: {path_3}")

path_4, dis1 = pathfinding.type_4(V, E, "a", "g")
print(
    f"type IV path (smallest distance) between a and g: {path_4} and their distance is: {dis1}\n"
)

path_5, dis2 = gurobi_solver.gurobi(V, E, "a", "g")
print(
    f"Solver Gurobi for type IV between a and g: {path_5} (may not be the same as the previous result) and their distance is: {dis2}"
)

print(
    "=================================================================================="
)
print("Describe the graph below (Usage: u,v,t,l):")
P2 = utils.readTerminal()

print(f"\nPath from the terminal: {P2}")
