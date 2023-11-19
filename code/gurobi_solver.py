from gurobipy import Model, GRB, LinExpr
from collections import defaultdict


def gurobi(e, a, s, d):
    """
    Solves the shortest path problem using the Gurobi optimization solver.

    Args:
        e (list): A list of edges in the graph.
        a (list): A list of weighted arcs in the graph.
        s (str): The source vertex.
        d (str): The destination vertex.

    Returns:
        tuple: A tuple containing the path in the graph and the objective value of the model.
    """
    Nodes = []

    for j in e:
        m, n = j
        Nodes.append(str(m + str(n)))

    Arcs = {}

    for edge in a:
        a1, b1 = (edge.u[0], edge.u[1])
        t = str(a1 + str(b1))
        c1, d1 = (edge.v[0], edge.v[1])
        v = str(c1 + str(d1))
        v2 = edge.weight
        Arcs[(t, v)] = v2

    model = Model("spp problem")
    model.Params.LogToConsole = 0

    clustered_vertices = defaultdict(list)

    for i in e:
        clustered_vertices[i[0]].append(i)

    a2, b2 = clustered_vertices[s][0]
    c2, d2 = clustered_vertices[d][0]
    depart = str(a2 + str(b2))
    arrive = str(c2 + str(d2))

    # add decision variables
    X = {}
    for key in Arcs.keys():
        index = key[0] + "," + key[1]
        X[key] = model.addVar(vtype=GRB.BINARY, name=index)

    # add objective function
    obj = LinExpr(0)

    for key in Arcs.keys():
        obj.addTerms(Arcs[key], X[key])

    model.setObjective(obj, GRB.MINIMIZE)

    # constraint1 1 and constraint 2
    lhs_1 = LinExpr(0)
    lhs_2 = LinExpr(0)

    for key in Arcs.keys():
        if key[0] == depart:
            lhs_1.addTerms(1, X[key])
        elif key[1] == arrive:
            lhs_2.addTerms(1, X[key])

    model.addConstr(lhs_1 == 1, name="start flow")
    model.addConstr(lhs_2 == 1, name="end flow")

    # constraints 3
    for node in Nodes:
        lhs = LinExpr(0)
        if node != depart and node != arrive:
            for key in Arcs.keys():
                if key[1] == node:
                    lhs.addTerms(1, X[key])
                elif key[0] == node:
                    lhs.addTerms(-1, X[key])
        model.addConstr(lhs == 0, name="flow conservation")

    model.write("model_spp.lp")
    model.optimize()

    li = []
    li.append(depart)

    for var in model.getVars():
        if var.x > 0:
            t1, t2 = (var.varName).split(",")
            if t1 != depart and t2 != arrive:
                li.append(t1)
                li.append(t2)
    li.append(arrive)

    b = {}
    b = b.fromkeys(li)
    c = list(b.keys())

    tmp = []

    for i in c:
        ab, cd = list(i)
        tmp.append((str(ab), int(cd)))

    path_in_G = []

    for vertex in range(len(tmp) - 1):
        if tmp[vertex][0] != tmp[vertex + 1][0]:
            edge = (tmp[vertex][0], tmp[vertex + 1][0], tmp[vertex][1], 1)
            path_in_G.append(edge)

    return path_in_G, model.ObjVal
