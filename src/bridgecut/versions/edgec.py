"""
Edge Bridging Centrality.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.core import BridgeCut

class EdgeCBridgeCut(BridgeCut):
    
    def split(self, graph, d):
        """
        @see parent
        """
        edges = graph.edges()
        
        # No edges left...
        if not len(edges):
            return None, None, None
        
        btwns_ranks = self.ranks(edges, lambda edge: edge.btwns())
        bridge_ranks = self.ranks(edges, lambda edge: edge.bridge_coeff())

        ranks = sorted([(edge, btwns_ranks[edge] * bridge_ranks[edge]) for edge in edges], key=lambda v: v[1], reverse=True)
        
        if d > 1:
            # Find the top % of ranked items.
            edges = [rank[0] for rank in ranks[:int(len(ranks) * self.__class__.TIER + 1)]]
            # Iteratively find the ranks at each depth up to d.
            bridge_reranks = {}
            for edge in edges:
                bridge_reranks[edge] = bridge_ranks[edge]      
            for i in range(2, d + 1):
                tmp_ranks = self.ranks(edges, lambda edge: edge.bridge_coeff(i))
                for edge in tmp_ranks:
                    bridge_reranks[edge] += tmp_ranks[edge]
        
        # Determine the best edge.
        best_edge, best_score = self.tiebreak(ranks, lambda edge: edge.node1.deg() + edge.node2.deg())  
        
        return best_edge, best_score, best_edge.destroy()