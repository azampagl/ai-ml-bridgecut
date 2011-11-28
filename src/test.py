"""
Python implementation of Bridge Cut algorithm.

Bridging Centrality: Graph Mining
from Element Level to Group Level

@see http://dl.acm.org/citation.cfm?id=1401934

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 04, Bridge Cut
@requires Python >=2.4
@copyright 2011 Aaron Zampaglione
@license MIT
"""
from bridgecut.core import BridgeCut
from bridgecut.graph.core import Graph

import getopt
import sys

def main():
    """Main execution method."""
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], "i:o:v:t:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['i', 'o', 'v', 't']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    # Make sure the version exists.
    if not opts['v'] in BridgeCut.VERSIONS:
        usage()
        sys.exit(2)
    
    # Some people like spaces, other like tabs, some like \r\n, other like \n... etc.
    #  I personally think Dr. Chan can't make up his mind!
    #  and I'm also to lazy to use REGEX for this.
    items = [line.replace('\t', ' ').replace('\n', '').replace('\r', '').split(' ') for line in open(opts['i'], 'r')]
    while len(items[-1]) < 2:
        items.pop()
    
    # Make a graph.
    graph = Graph.factory(items)
    
    node = graph.node('2')
    
    #print(', '.join([str(n) for n in node.nbrh(d=2)]))
    print(graph.node('2').bridge_coeff(d=2))
    print(graph.node('1').bridge_coeff(d=2))
    '''
    # Execution of the specific version.
    results, clusters = BridgeCut.factory(opts['v'], graph).execute(float(opts['t']))
    
    # Performance measurements.
    davies_bouldin = BridgeCut.davies_bouldin(graph, clusters)
    silhouette = BridgeCut.silhouette(graph, clusters)
    
    output = 'Top Items Removed:\n\n'
    output += '\t#\t-\tItem\t-\tRank\t-\tNodes Removed\t-\tClustering Coefficient\n\n'
    i = 1
    for result in results:
        output += '\t' + str(i) + '.\t' + str(result[0]) + '\t-\t' + str(result[1]) + '\t-\t' + str(result[2]) + '\t-\t' + str(result[3]) + '\n'
        i += 1
    output += '\nClusters:\n\n'
    for cluster in clusters:
        output += '\t' + str(cluster) + '\n'
    
    output += '\n'
    output += 'DB Index:\t\t\t\t' + str(davies_bouldin) + '\n'
    output += 'Average Silhouette Coefficient:\t' + str(silhouette) + '\n'
    
    out = open(opts['o'], 'w')
    out.write(output)
    out.close()
    
    # Print out performance measurements for sensitivity analysis later.
    print('\t'.join([str(davies_bouldin), str(silhouette)]))
    '''

def usage():
    """Prints the usage of the program."""
    print("\n" + 
          "The following are arguments required:\n" + 
          "-i: the density threshold.\n" +
          "-o: the output file.\n" +
          "-v: the bridge cut version (" + ", ".join(BridgeCut.VERSIONS) + ").\n" + 
          "-t: the density threshold.\n" + 
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -i \"../data/toy/toy-bowtie.txt\" -o \"../results/toy/toy-bowtie.txt\" -d 0 -v \"edge-c\" -t .5" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()