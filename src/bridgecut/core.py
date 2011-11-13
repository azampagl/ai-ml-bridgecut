"""
@package bridgecut
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from exception import BridgeCutException
from lib.util import combinations, product

class BridgeCut(object):
    
    # Different versions of the algorithm..
    VERSIONS = {
                'edge-c': (['versions', 'edgec'], 'EdgeCBridgeCut'), # Edge with the highest Bridging Centrality.
                'edge-b': (['versions', 'edgeb'], 'EdgeBBridgeCut'), # Edge with the highest Betweenness.
                'vertex-c': (['versions', 'vertexc'], 'VertexCBridgeCut'), # Vertex with the highest Bridging Centrality.
                'vertex-b': (['versions', 'vertexb'], 'VertexBBridgeCut'), # Vertex with the highest Betweenness.
                }
       
    @classmethod
    def davies_bouldin(cls, graph, clusters):
        """
        Return the davies bouldin index for the clusters.
        
        Key arguments:
        graph    -- the original graph
        clusters -- the clusters to analyze
        """
            
        # If we only have one cluster, then return inf!
        if len(clusters) < 2:
            return float('inf')
        
        # Special case, if all the clusters are singletons, return inf.
        singletons = True
        for cluster in clusters:
            if len(cluster.nodes) > 1:
                singletons = False
                break
        
        if singletons:
            return float('inf')
        
        # Calculate the diameters for each cluster.
        diams = {}
        for cluster in clusters:
            diams[cluster] = 0.0
            if len(cluster.nodes) > 1:
                paths = cluster.paths()
                for node1, node2 in combinations(cluster.nodes, 2):
                    diams[cluster] = max(diams[cluster], cluster.dist(node1, node2, paths))
                
                # If it weren't for directed graphs, we could use the combinations method.
                for node1 in paths:
                    for node2 in paths[node1]:
                        if node1 != node2 and paths[node1][node2]:
                            diams[cluster] = max(diams[cluster], cluster.dist(node1, node2, paths))
        
        # Find all the graphs paths.
        paths = graph.paths()
        
        # Calculate the distances between each cluster.
        dists = {}
        for cluster1, cluster2 in combinations(clusters, 2):
            if not cluster1 in dists:
                dists[cluster1] = {}
            if not cluster2 in dists:
                dists[cluster2] = {}
                
            # Find the average cluster distance between cluster i and j.
            dist = sum([graph.dist(node1, node2, paths) for node1, node2 in product(cluster1.nodes, cluster2.nodes)]) / float(len(cluster1.nodes) * len(cluster2.nodes))
            dists[cluster1][cluster2] = dist
            dists[cluster2][cluster1] = dist
        
        num = 0.0
        for cluster1 in clusters:
            max_db = 0.0
            for cluster2 in clusters:
                if cluster1 != cluster2:
                    max_db = max(max_db, (diams[cluster1] + diams[cluster2]) / dists[cluster1][cluster2])
            num += max_db
            
        return num / len(clusters)
    
    @classmethod
    def factory(cls, v, graph):
        """
        Returns a specific version of the Bridge Cut algorithm.
        
        Key arguments:
        v     -- the version
        graph -- the inital graph.
        """
        if v in cls.VERSIONS:
            obj = None
            exec('import ' + '.'.join(cls.VERSIONS[v][0]))
            exec('obj = ' + '.'.join(cls.VERSIONS[v][0]) + '.' + cls.VERSIONS[v][1] + '(graph)')
            return obj
        
        raise BridgeCutException('Version Not Implemented.')
    
    @classmethod
    def silhouette(cls, graph, clusters):
        """
        Find the average silhouette distance for the clusters.
        """
        paths = graph.paths()
        
        # Calculate the distances for all pairs of nodes.
        dists = {}
        for node1, node2 in combinations(graph.nodes, 2):
            value1 = node1.value
            value2 = node2.value
            dist = graph.dist(node1, node2, paths)
                
            if not value1 in dists:
                dists[value1] = {}
            if not value2 in dists:
                dists[value2] = {}
                
            dists[value1][value2] = dist
            dists[value2][value1] = dist
        
        s = 0.0
        for node in graph.nodes:
            # Find a and b.
            a = 0.0
            b = float('inf')
            for cluster in clusters:
                if cluster.node(node.value):
                    if len(cluster.nodes) > 1:
                        a = sum([dists[node.value][onode.value] for onode in cluster.nodes if node.value != onode.value]) / float(len(cluster.nodes) - 1)
                    else:
                        a = 0.0
                else:
                    b = min(b, sum([dists[node.value][onode.value] for onode in cluster.nodes]) / float(len(cluster.nodes)))
            
            if b == float('inf'):
                b = 0.0
            
            s += (b - a) / max(a, b)
        
        return s / len(graph.nodes)
        
    def __init__(self, graph):
        """
        Init.
        
        Key arguments:
        graph -- the graph.
        """
        self.graph = graph
    
    def execute(self, t):
        """
        Cluster the graph based on bridges.
        
        Key arguments:
        t -- density threshold
        """
        # Deep copy the graph for multiple execution.
        graph = self.graph.copy()
        
        clusters = []
        results = []
        
        while graph.nodes:
            size = len(graph.nodes)
            top, score, nodes = self.split(graph)
            
            # There was nothing to be split,
            #  remove the node that tried to destroy.
            if not nodes:
                cluster = graph.__class__.expand(top)
                clusters.append(cluster)
                graph.remove(cluster)
                        
            while nodes:
                node = nodes.pop()
                # Expand this node.
                cluster = graph.__class__.expand(node)
                
                nodes = list(set(nodes).difference(cluster.nodes))
                
                if cluster.density() > t:
                    clusters.append(cluster)
                    graph.remove(cluster)
            
            # Append the top edge/vertex, score, nodes removed, and graph clustering coefficient.
            results.append((top, score, (size - len(graph.nodes)), graph.cluster_coeff()))
        
        return results, clusters
    
    def ranks(self, paths, items, func, deg):
        """
        Ranks the scores based on a given method.
        
        Key arguments:
        paths -- shortest paths in the graph.
        items -- the items that are to be ranked (nodes or edges).
        func  -- the scoring function.
        """
        scores = {}
        for item in items:
            score = func(item)
            if score in scores:
                scores[score].append(item)
            else:
                scores[score] = [item]
        
        ranks = {}
        rank = 1
        for score in sorted(scores.iterkeys()):
            # Sort the items by their degree.
            scores[score] = sorted(scores[score], key=deg, reverse=True)
            
            last_deg = deg(scores[score][0])
            for item in scores[score]:
                if deg(item) != last_deg:
                    rank += 1
                ranks[item] = rank
            rank += 1
        
        return ranks