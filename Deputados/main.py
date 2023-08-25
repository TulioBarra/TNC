from graph import Graph
from weightedGraph import WeightedGraph
import time

#===============================================================================#
# WEIGHTED GRAPHS                                                             #
#===============================================================================#
# Lesson 12 - Floyd-Warshall algorithm 
g = WeightedGraph()
g.read_file("datasets/floyd-warshall-test.txt")
print(g)
print(g.floyd_warshall())


# Lesson 11 - Shortest path algorithms performance comparison
# g = WeightedGraph()
# g.read_file("datasets/USA-road-dt.DC.txt")

# start_time = time.time()
# g.bellman_ford("0")
# print(f"{'Time elapsed (Bellman-Ford):':35} {time.time() - start_time:.3f}")

# start_time = time.time()
# g.bellman_ford_improved("0")
# print(f"{'Time elapsed (Bellman-Ford impr.):':35} {time.time() - start_time:.3f}")

# start_time = time.time()
# g.dijkstra("0")
# print(f"{'Time elapsed (Dijsktra):':35} {time.time() - start_time:.3f}")

# start_time = time.time()
# g.dijkstra_pq("0")
# print(f"{'Time elapsed (Dijsktra PQ):':35} {time.time() - start_time:.3f}")

# Lesson 10 - Shortest path algorithms
# g = WeightedGraph()
# g.read_file("USA-road-dt.DC.txt")
# start_time = time.time()
# g.bellman_ford("0")
# end_time = time.time()
# print("Time elapsed (BF Improved):", end_time - start_time)

# # Lesson 9 - Graph file reading
# g = WeightedGraph()
# g.read_file("graph1.txt")
# print(g)

# # Lesson 8 - Weighted graph creation
# g = WeightedGraph()
# g.add_node(0)
# g.add_node(1)
# g.add_node(2)
# g.add_edge(0, 2, 20)
# g.add_edge(1, 0, 12)
# g.add_edge(1, 2, 18)

#===============================================================================#
# UNWEIGHTED GRAPHS                                                             #
#===============================================================================#

# # Lesson 1 - Graph creation 
# g = Graph()
# g.add_node("Bia")
# g.add_node("Caio")
# g.add_node("Liz")
# g.add_node("Alex")

# g.add_edge("Caio", "Liz")
# g.add_edge("Caio", "Alex")
# g.add_edge("Liz", "Caio")
# g.add_edge("Alex", "Liz")
# print(g)

# # Lesson 2 - Degree-related methods
# print("Out-degree of node Liz:", g.degree_out("Liz"))
# print("In-degree of node Liz:", g.degree_in("Liz"))
# print("Highest out-degree:", g.highest_degree_out())
# print("Highest in-degree:", g.highest_degree_in())

# # Lesson 3 - Graph properties
# print("Density:", g.density())
# print("Is complete:", g.is_complete())
# print("There is edge (Caio, Liz):", g.there_is_edge("Caio", "Liz"))
# print("Neighbors of Caio:", g.neighbors("Caio"))
# print("Is oriented:", g.is_oriented())
# print("Is regular:", g.is_regular())

# # Lesson 4 - Graph properties (pt. 2)
# print("Complement of g:", g.complement()) 
# g2 = Graph()
# g2.add_nodes(["Bia", "Caio", "Alex"])
# g2.add_two_way_edge("Bia", "Caio")
# g2.add_two_way_edge("Alex", "Bia")
# print("Is subgraph of g2:", g.is_subgraph_of(g2))

# # Lesson 5 - Graph walks 
# g3 = Graph()
# g3.add_nodes([0, 1, 2, 3, 4, 5, 6])
# g3.add_two_way_edge(0, 1)
# g3.add_two_way_edge(0, 3)
# g3.add_two_way_edge(0, 5)
# g3.add_two_way_edge(1, 2)
# g3.add_two_way_edge(1, 3)
# g3.add_two_way_edge(2, 3)
# g3.add_two_way_edge(2, 6)
# g3.add_two_way_edge(3, 4)
# g3.add_two_way_edge(3, 5)
# g3.add_two_way_edge(3, 6)
# g3.add_two_way_edge(4, 5)
# g3.add_two_way_edge(4, 6)

# print("Walk 0 -> 3 -> 2 is valid?", g3.is_valid_walk([0, 3, 2]))
# print("Walk 0 -> 6 -> 2 is valid?", g3.is_valid_walk([0, 6, 2]))
# print("Path 0 -> 3 -> 2 is valid?", g3.is_valid_path([0, 3, 2]))
# print("Path 0 -> 3 -> 0 -> 1 is valid?", g3.is_valid_path([0, 3, 0, 1]))

# # Lesson 6 - Graph search
# g4 = Graph()
# g4.add_nodes([0, 1, 2, 3, 4, 5])
# g4.add_two_way_edge(0, 2)
# g4.add_two_way_edge(0, 5)
# g4.add_two_way_edge(2, 4)
# g4.add_two_way_edge(4, 3)
# g4.add_two_way_edge(4, 5)
# print("BFS from 0:", g4.bfs(0))
# print("DFS (recursive) from 0:", g4.dfs_rec(0))
# print("DFS from 0:", g4.dfs(0))
# print("g4 is connected?", g4.is_connected())