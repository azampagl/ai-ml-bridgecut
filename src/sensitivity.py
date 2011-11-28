"""
Sensitivity analysis for all versions of bridge cut
using the threshold parameters.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
import commands
import os

INPUT = '../data/lesmis/lesmis.txt'
OUTPUT = '../results/lesmis'

for d in range(1, 2):
    
    results = {'edge-c': {},
               'vertex-c': {},
            }
    
    start = 0
    stop = 0.96
    inc = 0.05
    
    DIR = OUTPUT + '/d' + str(d)
    
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    
    while start < stop:
        for version in results:
            cmd = 'python main.py ' + \
                  '-i "' + INPUT + '" ' + \
                  '-o "' + DIR + '/results-' + str(version) + \
                  '-' + str(start) + '.txt" ' + \
                  '-v ' + str(version) + ' ' + \
                  '-t ' + str(start) + ' ' + \
                  '-d ' + str(d)
        
            # Save our response
            _, response = commands.getstatusoutput(cmd)
            results[version][start] = commands.getstatusoutput(cmd)[1].split("\t")
        
        start += inc
    
    # Print excel like table for each metric (2).
    for index in range(2):
        output = 'DEPTH: ' + str(d)
        output += 'THRESH\t' + '\t'.join(results.keys()) + '\n'
        start = 0
        while start <= stop:
            output += str(start) + "\t"
            for algo, result in results.items():
                output += result[start][index] + '\t'
            output += '\n'
            start += inc
        print(output)
        print('')
    print('')