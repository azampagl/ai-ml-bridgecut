"""
Node of a graph.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.lib.util import combinations

from operator import mul

class Node(object):
    
    def __init__(self, value):
        """
        Init.
        
        Key arguments:
        value -- the value of this node.
        """
        self.value = value
        
        # Init node's edges.
        self.edges = []
    
    def __str__(self):
        """
        String representation of the node.
        """
        return self.value  
    
    def bridge_coeff(self, d=1):
        """
        Finds the bridging coefficient of this node.
        """        
        num = 0.0
        
        # Find the neighborhood at depth d.
        nbrh = self.nbrh(d=d)
        nbrd = self.nbrs(d=d)
        
        # No neighbors at this depth.
        if len(nbrd) == 0:
            return 0.0
        
        for n in nbrd:
            if n.deg() == 1:
                continue
            
            nbrs = list(nbrh)
            nbrs.remove(n)
            
            edges = set()
            for nbr in nbrs:
                edges.update(nbr.edges)
            
            num += len(set(n.edges).difference(edges)) / float(n.deg() - 1)
        
        return num / float(len(nbrd))
    
    def btwns(self):
        """
        Find the egocentric betweenness centrality for this node.
        """
        ret = 0.0
        
        # Find the neighbors of this node's neighbors.
        nbrs = {}
        for nbr in self.nbrs():
            nbrs[nbr] = nbr.nbrs()
        nbrs[self] = self.nbrs()
        
        # We need the node keys sorted properly to build a contact matrix.
        snodes = sorted(nbrs.keys())
        
        # Generate a contact matrix.
        cmatrix = []
        for node1 in snodes:
            cmatrix.append([int(node1 != node2 and node1 in nbrs[node2]) for node2 in snodes])
        
        for node1, node2 in combinations(snodes, 2):
            row = snodes.index(node1)
            col = snodes.index(node2)
            if not cmatrix[row][col]:
                s = sum(map(mul, cmatrix[row][:], cmatrix[:][col]))
                if s > 0:
                    ret += 1 / float(s)
        
        return ret    
    
    def deg(self, d=1):
        """
        Returns the degree of this node.
        
        Key arguments:
        d -- depth [optional]
        """
        return len(self.nbrs(d=d))
    
    def destroy(self):
        """
        Destroy's this node and returns all the direct neighbor nodes.
        """
        nbrs = self.nbrs()
        edges = list(self.edges)
        
        for edge in edges:
            edge.destroy()
        
        return nbrs
    
    def nbrh(self, d=1):
        """
        Finds the neighborhood up to a certain depth.
        
        Key arguments:
        d -- the depth.
        """
        nbrh = [self]
        
        visited = {}
        
        q = [(self, 1)]
            
        while q:
            node, depth = q.pop(0)
                
            # Add to visited list.
            visited[node] = None
                    
            for nbr in node.nbrs():
                if not nbr in visited:
                    if depth < d:
                        q.append((nbr, depth + 1))
                    nbrh.append(nbr)
        
        return nbrh
    
    def nbrs(self, n=None, d=1):
        """
        Finds this node's neighbors
        
        Additionally, if n is provided, only finds
        the neighbors that are common to this node and
        node n.
        
        Key arguments:
        n -- other node [optional]
        d -- depth [optional]
        """
        if d > 1:
            nbrs = []
            visited = {}
            
            q = [(self, 1)]
            
            while q:
                node, depth = q.pop(0)
                
                # Add to visited list.
                visited[node] = None
                    
                for nbr in node.nbrs():
                    if not nbr in visited:
                        if depth < d:
                            q.append((nbr, depth + 1))
                        elif depth == d and not nbr in nbrs:
                            nbrs.append(nbr)
        else:
            nbrs = [edge.node(self) for edge in self.edges]
        
        # Return common neighbors.
        if n:
            return list(set(nbrs).intersection(n.nbrs(d=d)))
        
        return nbrs