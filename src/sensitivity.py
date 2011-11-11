"""
Sensitivity analysis for all versions of bridge cut
using the threshold parameters.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
import commands

results = {'edge-c': {},
           'edge-b': {},
           'vertex-c': {},
           'vertex-b': {},
            }

start = 0
stop = 1.01
inc = 0.05

while start <= stop:
    for version in results:
        cmd = 'python main.py ' + \
              '-i "../data/enron/enron2.txt" ' + \
              '-o "../results/enron/enron2-' + str(version) + \
              '-' + str(start) + '.txt" ' + \
              '-v ' + str(version) + ' ' + \
              '-t ' + str(start)
    
        # Save our response
        _, response = commands.getstatusoutput(cmd)
        results[version][start] = commands.getstatusoutput(cmd)[1].split("\t")
    
    start += inc

# Print excel like table for each metric (2).
for index in range(2):
    output = 'THRESH\t' + '\t'.join(results.keys()) + '\n'
    start = 0
    while start <= stop:
        output += str(start) + "\t"
        for algo, result in results.items():
            output += result[start][index] + '\t'
        output += '\n'
        start += inc
    print(output)
    print('')