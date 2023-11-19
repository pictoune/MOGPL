def readTerminal():
    """
    Reads input from the terminal and returns a list of edges to describe a graph.

    Returns:
        list: A list of edges, where each edge is represented as a tuple (u, v, t, l).
    """
    P = []
    input_ = input()

    while input_ != "quit":
        tmp = input_.split(",")

        if len(tmp) != 4:
            print('Error. Usage: "u,v,t,l"')
            break

        u, v, t, l = tmp[0], tmp[1], int(tmp[2]), int(tmp[3])

        edge = (u, v, t, l)
        P.append(edge)

        input_ = input()

    return P


def readFile(name):
    """
    Reads a file and returns a list of edges.

    Args:
        name (str): The name of the file to read.

    Returns:
        list: A list of edges, where each edge is represented as a tuple (u, v, t, l).

    Raises:
        Exception: If the file is not found or cannot be read.
    """
    p = []

    try:
        with open(name, "r") as f:
            tmp = f.read()
            line_list = tmp.splitlines()
            nb_s = int(line_list[0])
            nb_a = int(line_list[1])

            for i in range(nb_s + 2, len(line_list)):
                tmp = line_list[i].split(",")
                u, v, t, l = tmp[0], tmp[1], int(tmp[2]), int(tmp[3])
                p.append((u, v, t, l))
    except Exception as e:
        print("File not found\n", e)

    return p
