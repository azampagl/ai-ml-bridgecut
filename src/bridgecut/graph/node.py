"""
Node of a graph.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.lib.util import combinations

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
    
    def bridge_coeff(self):
        """
        Finds the bridging coefficient of this node.
        """
        if self.deg() == 0:
            return 0.0
        
        num = 0.0
        
        # Find the neighborhood, including myself.
        nbrh = self.nbrs()
        nbrh.insert(0, self)
        
        for n in self.nbrs():
            if n.deg() == 1:
                continue
            
            nbrs = list(nbrh)
            nbrs.remove(n)
            edges = []
            for nbr in nbrs:
                edges.extend(nbr.edges)
            
            num += len(set(n.edges).difference(edges)) / float(n.deg() - 1)
        
        return num / float(self.deg())
    
    def btwns(self, paths):
        """
        Find the betweenness centrality for this node.
        
        Key arguments:
        paths -- a dictionary of all the shortest paths.
        """
        ret = 0.0
        
        for node1, node2 in combinations(paths.keys(), 2):
            # There theoretically can be no shortests paths if we deleted
            #  a bridge, but the density of the new clusters didn't meet the threshold.
            if node1 != self and node2 != self and paths[node1][node2]:
                # Look at all shortest paths from node1 to node2.
                ret += sum([1 for path in paths[node1][node2] if self in path]) / float(len(paths[node1][node2]))
        
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
            nbrs = self.nbrs(None, d - 1)
            enbrs = set()
            for nbr in nbrs:
                enbrs.union(nbr.nbrs(None, d - 1))
            nbrs.append(self)
            nbrs = enbrs.difference(nbrs)
        else:
            nbrs = set()
            for edge in self.edges:
                nbrs.union(edge.node(self))
        
        # Return common neighbors.
        if n:
            return list(nbrs.intersection(n.nbrs(d=d)))
            
        return list(nbrs)