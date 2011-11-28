"""
Vertex Bridging Centrality.

@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.core import BridgeCut

class VertexCBridgeCut(BridgeCut):
    
    def split(self, graph, d):
        """
        @see parent
        """
        # Get all the shortest paths.
        paths = graph.paths()
        nodes = graph.nodes
        
        btwns_ranks = self.ranks(paths, nodes, lambda node: node.btwns(paths))
        bridge_ranks = self.ranks(paths, nodes, lambda node: node.bridge_coeff())
        
        ranks = sorted([(node, btwns_ranks[node] * bridge_ranks[node]) for node in nodes], key=lambda v: v[1], reverse=True)
        
        if d > 1:
            # Find the top % of ranked items.
            nodes = [rank[0] for rank in ranks[:int(len(ranks) * self.__class__.TIER + 1)]]
            # Iteratively find the ranks at each depth up to d.
            bridge_reranks = {}
            for node in nodes:
                bridge_reranks[node] = bridge_ranks[node]      
            for i in range(2, d + 1):
                tmp_ranks = self.ranks(paths, nodes, lambda node: node.bridge_coeff(i))
                for node in tmp_ranks:
                    bridge_reranks[node] += tmp_ranks[node]
            # Find the new ranks.
            ranks = sorted([(node, btwns_ranks[node] * bridge_reranks[node]) for node in nodes], key=lambda v: v[1], reverse=True)
        
        # Determine the best node.
        best_node, best_score = self.tiebreak(ranks, lambda node: node.deg())        
        
        nodes = best_node.destroy()
        
        # Remove this node from the graph.
        graph.nodes.remove(best_node)
        del graph.values[best_node.value]
        
        return best_node, best_score, nodes