"""
Converts a GML data file into a data file readable by our program.

@author Aaron Zampaglione <azampagl@azampagl.com>
@copyright 2011 Aaron Zampaglione
@license MIT
"""
import netconv

n = netconv.Network()
netconv.importGML(n, 'polbooks.gml')

print(len(n.getAllNodes()))

out = open('polbooks.txt', 'a')
for pair in n.toList():
    out.write(pair[0] + '\t' + pair[1] + '\n')
out.close()