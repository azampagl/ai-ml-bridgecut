============================================
Python BridgeCut

Aaron Zampaglione <azampagl@my.fit.edu>
CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
Proj 05, Bridge Cut Improvement
Python >=2.4
(c) 2011 Aaron Zampaglione
============================================

Python implementation of the original Bridge Cut algorithm.

Localized Bridging Centrality for Distributed Network Analysis
Soumendra Nanda and David Kotz
Department of Computer Science and Institute for Security Technology Studies
Dartmouth College, Hanover, NH 03755

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

> python main.py -i "../data/etc/big-bowtie.txt" -o "../results/etc/big-bowtie.txt" -v "edge-c" -t .5
