# MOGPL
This repository presents a project I completed (with another student) as a part of my master's course in modeling, optimization, graphs, linear programming (http://androide.lip6.fr/?q=node/23). This project explores the concept of finding various types of minimal paths in a directed multigraph weighted by time constraints. The multigraph represents an airline transport network where each vertex denotes an airport and the weight on each edge signifies the departure day of a flight.

## Types of Minimal Paths
The project defines four types of minimal paths in a time-weighted multigraph:
1. **Earliest Arrival Path**: A path that ensures the earliest arrival at the destination.
2. **Latest Departure Path**: A path that allows for the latest departure while reaching the destination before a given time.
3. **Fastest Path**: The path that takes the least amount of time to travel from source to destination.
4. **Shortest Path**: The path with the minimum total traversal time.

## Questions Explored
The project delves into several questions:
- Demonstrating that certain sub-paths of minimal paths may not be minimal.
- Transforming the time-weighted multigraph into a classic graph and calculating the four types of minimal paths.
- Analyzing the complexity of different proposed algorithms.
- Implementing a program to find the 4 types of minimal paths.
- Modeling the shortest path problem using linear programming and implementing a solution using GUROBI.
- Conducting tests to measure the execution time of the algorithm relative to the input size.
- Comparing the implemented algorithms for calculating Type IV paths.

## License
This project is open source and available under the [MIT License](LICENSE).

Feel free to explore the projects and reach out if you have any questions or suggestions.
