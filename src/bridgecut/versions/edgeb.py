"""
Edge Betweenness Centrality.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.core import BridgeCut

class EdgeBBridgeCut(BridgeCut):
    
    def split(self, graph):
        """
        @see parent
        """
        # Get all the shortest paths.
        paths = graph.paths()
        edges = graph.edges()
        
        btwns_ranks = self.ranks(paths, edges, lambda edge: edge.btwns(paths), lambda edge: edge.node1.deg() + edge.node2.deg())
        
        max_score = 0.0
        max_edge = None
        
        # Find the edge with the best score.
        for edge in edges:
            score = btwns_ranks[edge]
            if score > max_score:
                max_score = score
                max_edge = edge
        
        if not max_edge:
            return None, None, graph.nodes[0]
        
        return max_edge, max_score, max_edge.destroy()