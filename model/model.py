import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.nodes = DAO.getAllNodes()
        self.idMap = {}
        for v in self.nodes:
            self.idMap[v.object_id] = v
        self._allEdges = None
        self._bestPath = []
        self._bestCost = 0


    def getOptPath(self,source,lun):
        self._bestPath = []
        self._bestCost = 0

        parziale = [source]

        for n in nx.neighbors(self._graph,source):
            if parziale[0].classification == n.classification:
                parziale.append(n)
                self.ricorsione(parziale, lun)
                parziale.pop()

        return self._bestPath, self._bestCost


    def ricorsione(self,parziale,lun):
        if len(parziale) == lun:# parziale ha la lunghezza desiderata--> devo uscire
            if self.costo(parziale) > self._bestCost:
                self._bestCost = self.costo(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return
        #parziale puo ancora ammetter altri nodi
        for n in self._graph.neighbors(parziale[-1]):
            if parziale[-1].classification == n.classification and n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale, lun)
                parziale.pop()


    def costo(self, listObjects):
        totCost = 0
        for i in range(0, len(listObjects)-1):
            totCost += self._graph[listObjects[i]][listObjects[i+1]]["weight"]
        return totCost






    def buildGraph(self):

        self._graph.add_nodes_from(self.nodes)
        self.addAllEdges()


    def addEdgesV1(self):
        for u in self.nodes:
            for v in self.nodes:
                peso = DAO.getPeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)

    def addAllEdges(self):
        self._allEdges = DAO.getAllArchi(self.idMap)
        for e in self._allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getInfoConnessa(self, idInput: int):
        """
        Identifica la componente connessa e ne restituisce la dimensione
        """
        if not self.hasNode(idInput):
            return None
        source = self.idMap[idInput]
        # modo 1 conto i successori
        succ = nx.dfs_successors(self._graph, source).values()
        res = []
        for s in succ:
            res.extend(s)
        print("size connessa con modo 1:", len(res))

        #modo 2 conto i predecessori
        pred = nx.dfs_predecessors(self._graph, source)
        print("size connessa con modo 2:", len(pred.values()))

        #modo 3 conto i nodi dell'albero di visita (ho anche il source)
        dfsTree = nx.dfs_tree(self._graph, source)
        print("size connessa con modo 3:", len(dfsTree.nodes()))

        #modo 4 usi il metodo nodes connected components di networkx
        conn = nx.node_connected_component(self._graph, source)
        print("size connessa con modo 4:", len(conn))

        return len(conn)


    def hasNode(self, idInput: int):
        return idInput in self.idMap




    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)
        #return len(self._allEdges)

    def getIdMap(self):
        return self.idMap

    def getObjectFromId(self,id):
        return self.idMap[id]

