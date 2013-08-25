An attempt to determine important parts in a graph

Original algorithm based on:
Bridging Centrality: Graph Mining
from Element Level to Group Level
@see http://dl.acm.org/citation.cfm?id=1401934

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/


============================================
Arguments for python main.py
============================================

	The following are arguments required:

-i: the density threshold.
-o: the output file.
-v: the bridge cut version (vertex-c, vertex-b, edge-b, edge-c).
-t: the density threshold.


============================================
Execution
============================================

	Execution is straightforward.  After choosing a density threshold (-t), a version (-v), and an input file (-i) the program will spit out the clusters to the output file (-o).


======================
	Usage
======================

	The following are some example use cases.

> python main.py -i "../data/toy/toy-bowtie.txt" -o "../results/toy/toy-bowtie.txt" -d 0 -v "edge-c" -t .5
