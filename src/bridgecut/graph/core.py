"""
Graph core.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from node import Node
from edge import Edge

from bridgecut.lib.util import combinations

class Graph(object):
    
    @classmethod
    def expand(cls, node):
        """
        Builds a graph based on a single node by expanding.
        
        Key arguments:
        node  -- the node to expand.
        """
        visited = {}
        
        q = [node]
        while q:
            node = q.pop(0)
            visited[node.value] = node
            for nbr in node.nbrs():
                if not nbr.value in visited:
                    q.append(nbr)
        
        return cls(visited)
    
    @classmethod
    def factory(cls, items):
        """
        Returns a new graph.
        
        Key arguments:
        items -- the items to parse.
        """
        nodes = {}
        edges = {}
        
        for value1, value2 in items:
            node1 = None
            node2 = None
            
            try:
                node1 = nodes[value1]
            except KeyError:
                node1 = nodes[value1] = Node(value1)
            
            try:
                node2 = nodes[value2]
            except KeyError:
                node2 = nodes[value2] = Node(value2)
            
            if not node1 in edges:
                edges[node1] = {}
            if not node2 in edges:
                edges[node2] = {}
            
            if not node2 in edges[node1]:
                edges[node1][node2] = edges[node2][node1] = Edge(node1, node2)
        
        return cls(nodes)
    
    def __init__(self, nodes):
        """
        Init.
        
        Key arguments:
        nodes -- this graph's nodes.
        """
        # Go in order so we have the same results for every run regardless
        #  of ties.
        self.nodes = []
        for value in sorted(nodes.iterkeys()):
            self.nodes.append(nodes[value])      
        
        # Hashtable based on node values.
        self.values = nodes
    
    def __str__(self):
        """
        Returns graph as a string representation.
        """
        return ', '.join([str(node) for node in self.nodes])
    
    def bfs(self, src, paths):
        """
        BFS for all the shortest paths from a source node.
        
        Optimized this method as best as possible...
        
        Key arguments:
        src   -- source node
        paths -- already determined paths
        """
        newpaths = {}
        newpaths[src] = {}
        
        # All paths are guaranteed, so prebuild an empty dictionary.
        for node in self.nodes:
            if src != node:
                newpaths[src][node] = None
        
        # Keep track of nodes we have visited already.
        visited = {}
        visited[src] = True
        
        # BFS
        q = [(src, [])]
        while q:
            node, path = q.pop(0)
                    
            for nbr in node.nbrs():
                if not nbr in paths and nbr != src:
                    if newpaths[src][nbr] != None:
                        l1 = len(path)
                        l2 = len(newpaths[src][nbr][0])                    
                        # New shortest path!
                        if l1 < l2:
                            newpaths[src][nbr] = [list(path)]
                        # Add another shortest path.
                        elif l1 == l2:
                            newpaths[src][nbr].append(list(path))
                    else:
                        newpaths[src][nbr] = [list(path)]
                
                # Have we found paths to every node in the graph yet?
                if not nbr in visited:
                    visited[nbr] = True
                    # Add node to the new path.
                    newpath = list(path)
                    newpath.append(nbr)
                    # Add  to queue.
                    q.append((nbr, newpath))
        
        return newpaths
    
    def cluster_coeff(self):
        """
        Find the clustering coefficient.
        """
        if len(self.nodes) < 2:
            return 0.0
        
        num = 0.0
        for node in self.nodes:
            # Special case, node with only one neighbor.
            if node.deg() < 2:
                continue
            
            edges = set()
            for nbr1, nbr2 in combinations(node.nbrs(), 2):
                edges = edges.union(set(nbr1.edges).intersection(nbr2.edges))
            num += (2 * len(edges)) / float(node.deg() * (node.deg() - 1))
        
        return num / len(self.nodes)
    
    def copy(self):
        """
        Returns a deep copy of this graph.
        """
        items = []
        for node in self.nodes:
            for nbr in node.nbrs():
                items.append([node.value, nbr.value])
        
        return self.__class__.factory(items)
        
    def density(self):
        """
        Finds the density of this graph.
        """
        n = len(self.nodes)
        
        if (n - 1) == 0:
            return float('inf')
            
        return float(2 * len(self.edges())) / (n * (n - 1))
    
    def dist(self, node1, node2, paths=None):
        """
        Finds the distance between two nodes.
        
        Key arguments:
        node1 -- node1.
        node2 -- node2
        paths -- the shortest paths to compare against. [optional]
        """
        if not paths:
            paths = self.paths()
        
        # Make sure the nodes are in this graph!
        node1 = self.node(node1.value)
        node2 = self.node(node2.value)
        
        if not node1 or not node2:
            return float('inf')
        
        # We need to add one because the initial and final nodes of the route
        #  are not included in the actual route!
        return len(paths[node1][node2][0]) + 1.0
    
    def edges(self):
        """
        Returns the edges in the graph.
        """
        ret = set(self.nodes[0].edges)
        for node in self.nodes[1:]:
            ret = ret.union(node.edges)
        
        return list(ret)
        
    def node(self, value):
        """
        Returns the node based on a given value.
        
        Key arguments:
        value -- the value to return.
        """
        try:
            return self.values[value]
        except KeyError:
            return None
    
    def paths(self):
        """
        Finds all the shortest paths for every possible route.
        """
        paths = self.bfs(self.nodes[0], {})
        
        for node in self.nodes[1:]:
            paths.update(self.bfs(node, paths))
        
        # Build reverse ref.
        for i in range(len(self.nodes) - 1, 0, -1):
            for j in range(0, i):
                node1 = self.nodes[i] 
                node2 = self.nodes[j]
                paths[node1][node2] = paths[node2][node1]
          
        return paths
    
    def remove(self, graph):
        """
        Removes a graphs nodes from this one.
        
        Key arguments:
        graph -- the sub graph to remove nodes by.
        """
        for node in list(graph.nodes):
            self.nodes.remove(self.node(node.value))
            del self.values[node.value]