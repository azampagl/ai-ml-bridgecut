"""
Vertex Betweenness Centrality.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.core import BridgeCut

class VertexBBridgeCut(BridgeCut):
    
    def split(self, graph, d):
        """
        @see parent
        """
        nodes = graph.nodes
        
        btwns_ranks = self.ranks(nodes, lambda node: node.btwns())
        
        ranks = sorted([(node, btwns_ranks[node]) for node in nodes], key=lambda v: v[1], reverse=True)
        
        # Determine the best node.
        best_node, best_score = self.tiebreak(ranks, lambda node: node.deg())
        
        nodes = best_node.destroy()
        
        # Remove this node from the graph.
        graph.nodes.remove(best_node)
        del graph.values[best_node.value]
        
        return best_node, best_score, nodes