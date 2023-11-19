import matplotlib.pyplot as plt
import numpy as np
import time

import pathfinding
import graph


def measure_execution_time(range_values, nb_iter, graph_params_func, pathfinding_func):
    """
    Measure the execution time of a pathfinding algorithm for different graph parameters.

    Args:
            range_values (Iterable): The range of values for the graph parameters.
            nb_iter (int): The number of iterations to perform for each graph parameter.
            graph_params_func (Callable): A function that generates graph parameters based on a given value.
            pathfinding_func (Callable): The pathfinding algorithm to measure the execution time of.

    Returns:
            dict: A dictionary containing the minimum, mean, and maximum execution times for each graph parameter.
    """
    times = {"minimums": [], "means": [], "maximums": []}

    for value in range_values:
        values = [
            time_execution(graph_params_func, value, pathfinding_func)
            for _ in range(nb_iter)
        ]
        times["minimums"].append(np.min(values))
        times["means"].append(np.mean(values))
        times["maximums"].append(np.max(values))

    return times


def time_execution(graph_params_func, value, pathfinding_func):
    """
    Measure the execution time of a pathfinding algorithm for a given graph.

    Args:
            graph_params_func (Callable): A function that generates graph parameters based on a given value.
            value: The value used to generate the graph parameters.
            pathfinding_func (Callable): The pathfinding algorithm to measure the execution time of.

    Returns:
            float: The execution time of the pathfinding algorithm.
    """
    P = graph_params_func(value)
    V, E = graph.buildGraph(P)

    t0 = time.time()
    _, _ = pathfinding_func(V, E)
    t1 = time.time() - t0

    return t1


def plot_results(range_values, times, xlabel):
    """
    Plots the results of a performance analysis.

    Args:
        range_values (list): The range of values for the x-axis.
        times (dict): A dictionary containing the mean, minimum, and maximum times.
        xlabel (str): The label for the x-axis.
    """
    plt.plot(range_values, times["means"], color="deepskyblue")
    plt.fill_between(
        range_values, times["minimums"], times["maximums"], color="lightskyblue"
    )
    plt.xlabel(xlabel)
    plt.ylabel("Durée (s)")
    plt.show()


# Measure execution time based on the number of vertices
range_nb_vertices = np.arange(10, 100, 10)
nb_iter = 15
times_vertices = measure_execution_time(
    range_nb_vertices,
    nb_iter,
    lambda x: graph.generate_graph_G(x, 3000),
    lambda V, E: pathfinding.type_4(V, E, "s0", "s" + str(x - 1)),
)
plot_results(range_nb_vertices, times_vertices, "Nombre de sommets")

# Measure execution time based on the number of edges
range_nb_edges = np.arange(1001, 1500, 100)
times_edges = measure_execution_time(
    range_nb_edges,
    nb_iter,
    lambda x: graph.generate_graph_G(100, x),
    lambda V, E: pathfinding.type_4(V, E, "s0", "s98"),
)
plot_results(range_nb_edges, times_edges, "Nombre d'arrête")
