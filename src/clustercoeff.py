"""
@author Aaron Zampaglione <azampagl@my.fit.edu>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
VERSIONS = {'edge-c': '../results/enron/enron2-edge-c-0.6.txt',
           'edge-b': '../results/enron/enron2-edge-b-0.6.txt',
           'vertex-c': '../results/enron/enron2-vertex-c-0.6.txt',
           'vertex-b': '../results/enron/enron2-vertex-b-0.6.txt',
            }

NUM_NODES = 100

results = {'edge-c': {},
           'edge-b': {},
           'vertex-c': {},
           'vertex-b': {},
           }

for version, file_name in VERSIONS.iteritems():
    nodes = 0.0
    handle = open(file_name, 'r')
    for line in handle:
        line = line.rsplit('-', 3)
        if len(line) != 4:
            continue
        try:
            nodes += float(line[2].replace('\t', ''))
        except:
            continue
        p = str(nodes / NUM_NODES) 
        if not p in results[version]:
            results[version][p] = line[3][:-1].replace('\t', '')
    handle.close()

for version, result in results.iteritems():
    print(version)
    print("% Removed\tClustering Coefficient")
    for p, score in sorted(result.iteritems()):
        print(p + '\t' + score)
    print('')