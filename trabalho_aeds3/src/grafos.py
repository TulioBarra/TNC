class Grafos:
    def __init__(self) -> None:
        self.adj_list = {}
        self.node_count = 0
        
    def add_node(self, node):
        if node in self.adj_list:
            print("Esse nó já existe!")
            return
        self.adj_list[node] = []
        self.node_count+=1
        
    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)
            
    def list_nodes(self):
        for node in self.nodes:
            print(node)