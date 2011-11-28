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