"""
Vertex Betweenness Centrality.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.core import BridgeCut

class VertexBBridgeCut(BridgeCut):
    
    def split(self, graph):
        """
        @see parent
        """
        # Get all the shortest paths.
        paths = graph.paths()
        nodes = graph.nodes
        
        btwns_ranks = self.ranks(paths, nodes, lambda node: node.btwns(paths), lambda node: node.deg())
        
        max_score = 0.0
        max_node = None
        
        # Find the edge with the best score.
        for node in nodes:
            score = btwns_ranks[node]
            if score > max_score:
                max_score = score
                max_node = node
        
        # Find the nodes that were broken off.
        nodes = max_node.destroy()
        if nodes:
            nodes.append(max_node)
                
        return max_node, max_score, nodes