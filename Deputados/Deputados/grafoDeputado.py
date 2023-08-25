
class grafoDeputado:
    
    def __init__(self) -> None:
        self.adj_list = {}
        self.votacoes_deputado = {}
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, node):
        if node in self.adj_list:
            print(f"WARN: Node {node} already exists")
            return
        self.adj_list[node] = {}
        self.node_count += 1

    def add_edge(self, node1, node2):
        if node1 not in self.adj_list:
            self.add_node(node1)
        if node2 not in self.adj_list:
            self.add_node(node2)
        if node2 not in self.adj_list[node1]:
             self.adj_list[node1][node2] = 0
             self.edge_count += 1
        self.adj_list[node1][node2] += 1
        
    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_two_way_edge(self, node1, node2):
        self.add_edge(node1, node2)
        self.add_edge(node2, node1)

    def salvar_grafo(self, arq):
        with open(arq, 'w') as arq:
            linha = f"{self.node_count} {self.edge_count}\n"
            arq.write(linha)
            for vertice, arestas in self.adj_list.items():
                linha = ""
                for destino, peso in arestas.items():
                    v = vertice.replace(" ", "_")
                    d = destino.replace(" ", "_")
                    linha += f"{v} {d} {peso}\n"
                arq.write(linha)
        arq.close()

    def add_deputado(self, nome):
        if nome not in self.votacoes_deputado:
            self.votacoes_deputado[nome] = 0
        self.votacoes_deputado[nome] += 1

    def salvar_votacoes(self, arq):
        with open(arq, 'w') as arq:
            linha = ""
            for chave, valor in self.votacoes_deputado.items():
                c = chave.replace(" ", "_")
                linha = f"{c} {valor}\n"
                arq.write(linha)
        arq.close()

    def add_grafo(self, list, nome):
        for dp in list:
            self.add_two_way_edge(dp, nome)
        list.append(nome)           









