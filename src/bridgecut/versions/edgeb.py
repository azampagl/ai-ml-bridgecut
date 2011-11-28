"""
Edge Betweenness Centrality.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.core import BridgeCut

class EdgeBBridgeCut(BridgeCut):
    
    def split(self, graph, d):
        """
        @see parent
        """
        edges = graph.edges()
        
        btwns_ranks = self.ranks(edges, lambda edge: edge.btwns())
        
        ranks = sorted([(edge, btwns_ranks[edge]) for edge in edges], key=lambda v: v[1], reverse=True)
        
        # Determine the best edge.
        best_edge, best_score = self.tiebreak(ranks, lambda edge: edge.node1.deg() + edge.node2.deg())  
        
        return best_edge, best_score, best_edge.destroy()