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
    
    def bridge_coeff(self):
        """
        Finds the bridging coefficient of this edge.
        """
        num = self.node1.deg() * self.node1.bridge_coeff() + \
              self.node2.deg() * self.node2.bridge_coeff()
        
        den = (self.node1.deg() + self.node2.deg()) * \
              (len(self.node1.nbrs(self.node2)) + 1)
        
        return num / float(den)
    
    def btwns(self, paths):
        """
        Find the betweenness centrality for this edge.
        
        Key arguments:
        paths -- a dictionary of all the shortest paths.
        """
        ret = 0.0
        
        for node1, node2 in combinations(paths.keys(), 2):
            # There theoretically can be no shortests paths if we deleted
            #  a bridge, but the density of the new clusters didn't meet the threshold.
            if paths[node1][node2] != None:
                # A direct path from one to another still counts as a shortest path.
                if len(paths[node1][node2]) == 0:
                    ret += 1.0
                else:
                    ret += sum([1 for path in paths[node1][node2] if self.node1 in path and self.node2 in path]) / float(len(paths[node1][node2]))
        
        return ret
    
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