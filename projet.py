# -*- coding: utf-8 -*-
from collections import defaultdict 
from gurobipy import *
import numpy as np

# Authors: Xinan SHAO & Victor PIRIOU

class Edge:
	u = ()      # source
	v = ()      # destination
	weight = 0  

	def __init__(self, u, v, weight):
		self.u = u
		self.v = v
		self.weight = weight

# Bellman-Ford algorithm
def bellman_ford(vertices, edges, start, end):
	distances = {}
	parents = {}

	# initialisation
	for v in vertices:
		if v == start:
			distances[v] = 0
		else:
			distances[v] = float('inf')

	for i in range(len(vertices)-1):
		for edge in edges: 
			if distances[edge.u] + edge.weight < distances[edge.v]:
				distances[edge.v] = distances[edge.u] + edge.weight
				parents[edge.v] = edge.u

	distance = distances[end]

	if (end in parents):
		parent = parents[end]
		path = [parent, end]
		while parent != start:
			path.insert(0, parents[parent])
			parent = parents[parent]

		return distance, path
	else:
		print("No path found")
		return float('inf'),{}


def dijkstra(vertices, edges, start, end):
	nodes = {}

	# initialisation
	for vertex in vertices:
		nodes[vertex] = {}
		nodes[vertex]["distance"] = np.inf
		nodes[vertex]["visited"] = False
		nodes[vertex]["predecessor"] = None

	nodes[start]["predecessor"] = None
	nodes[start]["distance"] = 0

	nb_visited_nodes = 0

	while(nb_visited_nodes < len(vertices)):
		# here we determine which node has the smallest distance and we select it =======
		min_dist = np.inf

		for node_id in nodes.keys():
			if not nodes[node_id]["visited"]:
				if(nodes[node_id]["distance"] < min_dist):
					min_dist = nodes[node_id]["distance"]
					selected_node = node_id
		
		nodes[selected_node]["visited"] = True
		
		nb_visited_nodes += 1
		# ===============================================================================

		# for each of its unexplored neighbors, we update the distance ==================
		for edge in edges:
			if((selected_node == edge.u) and (not nodes[edge.v]["visited"])):
				neighbor = edge.v

				if(nodes[neighbor]["distance"] > nodes[edge.u]["distance"] + edge.weight):

					nodes[neighbor]["distance"] = nodes[edge.u]["distance"] + edge.weight

					nodes[neighbor]["predecessor"] = edge.u 
		# ===============================================================================

	# if we found a path
	if(nodes[end]["distance"] != np.inf):
		parent = nodes[end]["predecessor"]
		path = [parent,end]

		while parent != start:
			path.insert(0, nodes[parent]["predecessor"])
			parent = nodes[parent]["predecessor"]

		return nodes[end]["distance"], path
	else:
		print("No path found")
		return float('inf'),{}



def buildGraph(P):
	edges = []
	vertices = []

	for i in P:
		u,v,t,l = i
		
		if (u,t) not in vertices:
			vertices.append((u,t)) 
		
		if (v,t+l) not in vertices:
			vertices.append((v,t+l))

		edge = Edge((u,t),(v,t+l),l)

		edges.append(edge) # adds edges weighted by 1

	clustered_vertices = defaultdict(list)

	# adds edges weighted by 0 
	for e in vertices:
		clustered_vertices[e[0]].append(e)

	for i in clustered_vertices.keys():
		for j in range(len(clustered_vertices[i])-1):
			edges.append( Edge( clustered_vertices[i][j],clustered_vertices[i][j+1],0))

	return vertices,edges

	
# type I path: earliest arrival 
def type_1(vertices,edges,start,end):
	clustered_vertices = defaultdict(list)

	for vertex in vertices:
		clustered_vertices[vertex[0]].append(vertex)

	source = min(clustered_vertices[start], key=lambda k:k[1])
	destinations = sorted(clustered_vertices[end], key=lambda k:k[1])
	
	path_found = False

	for destination in destinations:
		_,path = bellman_ford(vertices,edges,source,destination)
		if path == {}:
			pass
		else:
			path_found = True
			break

	path_in_G = []

	if(path_found):
		for vertex in range(len(path)-1):
			if(path[vertex][0] != path[vertex+1][0]):
				edge = (path[vertex][0],path[vertex+1][0],path[vertex][1],1)

				path_in_G.append(edge)
		return path_in_G
	else:
		return None


# type II path: departure at the latest
def type_2(vertices,edges,start,end):
	clustered_vertices = defaultdict(list)
	
	for vertex in vertices:
		clustered_vertices[vertex[0]].append(vertex)

	sources = sorted(clustered_vertices[start], key=lambda k:k[1],reverse=True)
	destination = max(clustered_vertices[end], key=lambda k:k[1])

	path_found = False

	for source in sources:
		_,path = bellman_ford(vertices,edges,source,destination)
		if path == {}:
			pass
		else:
			path_found = True
			break

	path_in_G = []
	if(path_found):
		for vertex in range(len(path)-1):
			if(path[vertex][0] != path[vertex+1][0]):
				edge = (path[vertex][0],path[vertex+1][0],path[vertex][1],1)

				path_in_G.append(edge)
		return path_in_G
	else:
		return None

# type III path: shortest duration
def type_3(vertices,edges,start,end):
	clustered_vertices = defaultdict(list)

	for vertex in vertices:
		clustered_vertices[vertex[0]].append(vertex)

	sources = clustered_vertices[start]
	destinations = clustered_vertices[end]
	dictemps = defaultdict(list)

	for source in sources:
		for destination in destinations:
			_,t1 = source
			_,t2 = destination

			if t2>t1:
				dictemps[t2-t1].append((source,destination))

	tri = sorted(dictemps.items(),key=lambda k:k[0])

	for key in range(len(tri)):
		_,possible_paths = tri[key]

		for possible_path in possible_paths:
			source,destination = possible_path
			_,path = bellman_ford(vertices,edges,source,destination)
			if path == {}:
				pass
			else:
				path_found = True
				break

	path_in_G = []
	
	if(path_found):
		for vertex in range(len(path)-1):
			if(path[vertex][0] != path[vertex+1][0]):
				edge = (path[vertex][0],path[vertex+1][0],path[vertex][1],1)
				path_in_G.append(edge)
		return path_in_G
	else:
		return None			


# type IV path: smallest distance 
def type_4(e,a,s,d):
	def get_key (dict, value):
		return [k for k, v in dict.items() if value in v]
	clustered_vertices = defaultdict(list)

	for i in e:
		clustered_vertices[i[0]].append(i)

	dis,path = bellman_ford(e,a,clustered_vertices[s][0],clustered_vertices[d][0])
    
	path_in_G = []

	for vertex in range(len(path)-1):
		if(path[vertex][0] != path[vertex+1][0]):
			edge = (path[vertex][0],path[vertex+1][0],path[vertex][1],1)
			path_in_G.append(edge)
	return path_in_G,dis

# allows to specify a path from the terminal
# type "quit" to end 
def readTerminal():
	P = []
	input_ = input()
	while input_ != 'quit':
		tmp = input_.split(',')

		if(len(tmp) !=4):
			print('Error. Usage: "u,v,t,l"')
			break

		u,v,t,l = tmp[0],tmp[1],int(tmp[2]),int(tmp[3])

		edge = (u,v,t,l)
		P.append(edge);  

		input_ = input()
	return P

# reads a .txt file
def readFile(name):
	p = []
	try:
		with open(name,'r') as f:
			tmp = f.read()
			line_list = tmp.splitlines()
			nb_s = (int(line_list[0]))
			nb_a = (int(line_list[1]))
			for i in range(nb_s+2,len(line_list)):
				tmp = line_list[i].split(',')
				u,v,t,l = tmp[0],tmp[1],int(tmp[2]),int(tmp[3])
				p.append( (u,v,t,l) );  
	except Exception as e:
		print("File not found\n",e)
	return p


def gurobi(e,a,s,d):
    Nodes = []
    for j in e:
        m,n = j
        Nodes.append(str(m+str(n)))
    Arcs = {}
    for edge in a:
        a1,b1 = (edge.u[0],edge.u[1])
        t = str(a1+str(b1))
        c1,d1 = (edge.v[0],edge.v[1])
        v = str(c1+str(d1))
        v2 = edge.weight
        Arcs[(t,v)] = v2

    model = Model('spp problem') 
    model.Params.LogToConsole = 0

    clustered_vertices = defaultdict(list)
    for i in e:
        clustered_vertices[i[0]].append(i)
    
    a2,b2 = clustered_vertices[s][0]
    c2,d2 = clustered_vertices[d][0]
    depart = str(a2+str(b2))
    arrive = str(c2+str(d2))

    # add decision variables 
    X = {}
    for key in Arcs.keys():
        index =  (key[0]+','+key[1])
        X[key] = model.addVar( vtype=GRB.BINARY , name = index ) 

    # add objective function
    obj = LinExpr(0) 
    for key in Arcs.keys():
        # print(Arcs[key])
        obj.addTerms(Arcs[key], X[key])
    # print(obj)

    model.setObjective(obj, GRB.MINIMIZE) 

    # constraint1 1 and constraint 2  
    lhs_1 = LinExpr(0)
    lhs_2 = LinExpr(0)
    for key in Arcs.keys():
        if(key[0] == depart):
            lhs_1.addTerms(1, X[key])
        elif(key[1] == arrive):
            lhs_2.addTerms(1, X[key])
    model.addConstr(lhs_1 == 1, name = 'start flow')
    model.addConstr(lhs_2 == 1, name = 'end flow') 

    # constraints 3
    for node in Nodes:
        lhs = LinExpr(0)
        if( node != depart and node != arrive ):
            for key in Arcs.keys():
                if(key[1] == node):
                    lhs.addTerms(1, X[key])
                elif(key[0] == node):
                    lhs.addTerms(-1, X[key])
        model.addConstr(lhs == 0, name = 'flow conservation')  

    model.write('model_spp.lp')
    model.optimize()
    
    li = []
    li.append(depart)
    for var in model.getVars(): 
        if(var.x > 0):
            t1,t2 = (var.varName).split(',')
            if( t1 != depart and t2 != arrive):
                li.append(t1)
                li.append(t2)
    li.append(arrive)
    ### enlever des douplications 
    b={}
    b=b.fromkeys(li)
    c=list(b.keys())

    tmp = []
    for i in c:
        ab,cd = list(i)
        tmp.append((str(ab),int(cd)))

    path_in_G = []
    for vertex in range(len(tmp)-1):
        if(tmp[vertex][0] != tmp[vertex+1][0]):
            edge = (tmp[vertex][0],tmp[vertex+1][0],tmp[vertex][1],1)
            path_in_G.append(edge)
    return path_in_G, model.ObjVal


P1 = readFile('test.txt')
print('Path obtained from the file:',P1)


V,E = buildGraph(P1)

print("\n")
print("Vertices of G tilde: ",V)
print("\n")
print("Edges of G tilde:")

for edge in E:
	print("%s,%d"%(edge.u[0],edge.u[1])," => ","%s,%d"%(edge.v[0],edge.v[1]), " | weight =",edge.weight)

print("\n")

start = ('a', 1)
end = ('g', 8)
dijkstra(V, E, start, end)

import random

def generate_graph_G(nb_vertices,nb_edges):
	G = []

	for i in range(nb_edges):
		last_node = nb_vertices - 1

		starting_node = i%last_node
		end_node = random.randint(starting_node,starting_node + (starting_node+5)%(last_node+1))

		departure_date = random.randint(1,14)

		edge = ('s' + str(starting_node),'s' + str(end_node),departure_date,1)

		G.append(edge)

	return G

# TEMPS D'EXECUTION EN FONCTION DU NOMBRE DE SOMMETS
"""
import matplotlib.pyplot as plt
import time

range_nb_vertices = np.arange(10,100,10)

times = {}
times["minimums"] = []
times["means"] = []
times["maximums"] = []

nb_iter = 15

for nb_vertices in range_nb_vertices:
	values = []

	for i in range(nb_iter):
		P = generate_graph_G(nb_vertices,3000)

		V,E = buildGraph(P)

		t0= time.time()

		path_4,dis1 = type_4(V,E,'s0','s'+str(nb_vertices-1))

		t1 = time.time() - t0

		values.append(t1)

	times["minimums"].append(np.min(values))
	times["means"].append(np.mean(values))
	times["maximums"].append(np.max(values))

plt.plot(range_nb_vertices,times["means"], color="deepskyblue")
plt.fill_between(range_nb_vertices, times["minimums"], times["maximums"],color="lightskyblue")

plt.xlabel("Nombre de sommets")
plt.ylabel("Durée (s)")
#plt.title("Temps d'exécution sur " + str(nb_iter) + " itérations")
plt.show()	
"""
# ======================================================================================
# TEMPS D'EXECUTION EN FONCTION DU NOMBRE D'ARCS
"""
import matplotlib.pyplot as plt
import time

range_nb_edges = np.arange(1001,1500,100)

times = {}
times["minimums"] = []
times["means"] = []
times["maximums"] = []

nb_iter = 15

for nb_edges in range_nb_edges:
	values = []

	for i in range(nb_iter):
		P = generate_graph_G(100,nb_edges)

		V,E = buildGraph(P)

		t0= time.time()

		path_4,dis1 = type_4(V,E,'s0','s98')

		t1 = time.time() - t0

		values.append(t1)

	times["minimums"].append(np.min(values))
	times["means"].append(np.mean(values))
	times["maximums"].append(np.max(values))

plt.plot(range_nb_edges,times["means"], color="deepskyblue")
plt.fill_between(range_nb_edges, times["minimums"], times["maximums"],color="lightskyblue")

plt.xlabel("Nombre d'arrête'")
plt.ylabel("Durée (s)")
#plt.title("Temps d'exécution sur " + str(nb_iter) + " itérations")
plt.show()	
"""








path_1 = type_1(V,E,'a','c')
print("type I path (earliest arrival) between a and c : ",path_1)

path_2 = type_2(V,E,'a','g')
print("type II path (departure at the latest) between a and g : ",path_2)

path_3 = type_3(V,E,'a','g')
print("type III path (shortest duration) between a and g : ",path_3)

path_4,dis1 = type_4(V,E,'a','g')
print("type IV path (smallest distance) between a and g : ",path_4, " and their distance is :",dis1,"\n\n")

path_5,dis2 = gurobi(V,E,'a','g')
print("Solver Gurobi for type IV between a and g : ",path_5, " (may not be the same as the previous result) and their distance is :",dis2,"\n")

print("==================================================================================")

print("\nPath from the terminal:")

P2 = readTerminal()

print("\n",P2)
