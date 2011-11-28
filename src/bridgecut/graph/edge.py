"""
Edge of a graph.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.lib.util import combinations

class Edge(object):
    
    def __init__(self, node1, node2):
        """
        Init.
        
        Key arguments:
        node1 -- node 1
        node2 -- node 2
        """
        self.node1 = node1
        self.node2 = node2
        
        # Append this edge to the vertices.
        node1.edges.append(self)
        node2.edges.append(self)
    
    def __str__(self):
        """
        String representation of the edge.
        """
        return str(self.node1) + ' <-> ' + str(self.node2)
    
    def bridge_coeff(self, d=1):
        """
        Finds the bridging coefficient of this edge.
        
        Key arguments:
        d -- the depth [optional]
        """
        num = self.node1.deg(d) * self.node1.bridge_coeff(d) + \
              self.node2.deg(d) * self.node2.bridge_coeff(d)
        
        den = (self.node1.deg(d) + self.node2.deg(d)) * \
              (len(self.node1.nbrs(self.node2, d)) + 1)
        
        # Possibility that the nodes have 0 neighbors at depth d.
        if den == 0:
            return 0.0
        
        return num / float(den)
    
    def btwns(self):
        """
        Find the egocentric betweenness centrality for this edge.
        """
        return self.node1.btwns() + self.node2.btwns()
    
    def destroy(self):
        """
        Destroy's this edge and returns the two nodes that were part of it.
        """
        node1 = self.node1
        node2 = self.node2
        
        node1.edges.remove(self)
        node2.edges.remove(self)
        
        return [node1, node2]
    
    def node(self, node):
        """
        Returns the other node in this pair.
        
        Key arguments:
        node -- the node that we are NOT looking for.
        """
        if node == self.node1:
            return self.node2
        if node == self.node2:
            return self.node1
        
        return None