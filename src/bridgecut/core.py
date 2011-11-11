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
        #for node in clusters[-1].nodes:
        #    print(str(node) + ' ' + ', '.join([str(edge) for edge in node.edges]))
        
        #for cluster in clusters:
        #    print(cluster)
            
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
        
        #diams = {}
        #for cluster in clusters:
        #    diams[cluster] = 0.0
        #    if len(cluster.nodes) > 1:
        #        paths = cluster.paths()
                #for node1 in paths:
                #    for node2 in paths[node1]:
                        #print(paths[node1][node2])
                        #print(str(node1) + ' ' + ', '.join([str(key) for key in paths[node1].keys()]))
                #print('Done')
                #print(', '.join([str(node) for node in cluster.nodes]))
                #for node1, node2 in combinations(cluster.nodes, 2):
                #    print(str(node1) + ' ' + str(node2))
                #for nodea in paths:
                #    for nodeb in paths[nodea]:
                #        print(str(nodea) + ' ' + str(nodeb))
                #        print('\t' + ', '.join([str(node) for node in paths[nodea][nodeb][0]]))
                
                # If it weren't for directed graphs, we could use the combinations method.
                for node1 in paths:
                    for node2 in paths[node1]:
                        if node1 != node2 and paths[node1][node2]:
                            diams[cluster] = max(diams[cluster], cluster.dist(node1, node2, paths))
                #for node1, node2 in combinations(cluster.nodes, 2):
                #    # For directed, this path might not even exist.
                #    if node1 in paths and node2 in paths[node1] and paths[node1][node2]:
                #        diams[cluster] = max(diams[cluster], cluster.dist(node1, node2, paths))
        
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
            #print(graph)
            #print(size)
            #print('--')
            # Get the nodes after a split occurred.
            top, score, nodes = self.split(graph)
            #print(top)
            #if nodes:
            #    print(', '.join([str(node) for node in nodes]))
            #print('')
            
            # There was nothing to be split,
            #  remove the node that tried to destroy.
            if not nodes:
                cluster = graph.__class__.expand(top)
                clusters.append(cluster)
                graph.remove(cluster)
                        
            while nodes:
                node = nodes.pop()
                # Expand this node.
                #print('Graph Start Before:\t' + str(graph))
                cluster = graph.__class__.expand(node)
                #print('Graph Start After:\t' + str(graph))
                #print('Cluster:\t' + str(cluster))
                #print(cluster.density())
                #print(t)
                
                nodes = list(set(nodes).difference(cluster.nodes))
                # The new cluster might contain some of the nodes that
                #  were originally split.
                #values = list(set([node.value for node in nodes]).difference(cluster.values.keys()))
                #nodes = []
                #for value in values:
                #    nodes.append(graph.node(value))
                
                if cluster.density() > t:
                    #print('Graph Remove Before:\t' + str(graph))
                    #print('Cluster Remove Before:\t' + str(cluster))
                    clusters.append(cluster)
                    graph.remove(cluster)
                    #print('Graph Remove End:\t' + str(graph))
                    #print(str(node))
            
            # Append the top edge/vertex, score, nodes removed, and graph clustering coefficient.
            results.append((top, score, (size - len(graph.nodes)), graph.cluster_coeff()))
        
        return results, clusters
    
    def ranks(self, paths, items, func):
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
            for item in scores[score]:
                ranks[item] = rank
            rank += 1
        
        return ranks