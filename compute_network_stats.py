import argparse
import json
import os, sys
from pathlib import Path

import networkx as nx
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    inputfile = f'{args.input}'
    outputfile = f'{args.output}'
    with open(inputfile) as f:
        data = json.load(f)
    edgenum = {}
    for key in data:
        edgenum[key] = len(data[key])
    sortededgesnum = dict(sorted(edgenum.items(), key=lambda item: item[1], reverse=True))
    numlist = list(sortededgesnum.items())[:3]
    numlist2 = []
    for t in numlist:
        numlist2.append(t[0])
    weightsum = {}
    for key in data:
        weightsum[key] = sum(data[key].values())
    sortedweightsum = dict(sorted(weightsum.items(), key=lambda item: item[1], reverse=True))
    weightlist = list(sortedweightsum.items())[:3]
    weightlist2 = []
    for t in weightlist:
        weightlist2.append(t[0])
    for k, d in data.items():
        for i in d:
            d[i] = {'weight': d[i]}
    g = nx.DiGraph(data)
    between = nx.betweenness_centrality(g)
    #print(g['Twilight Sparkle']['Rainbow Dash']['weight'])
    sortedbetweeness = dict(sorted(between.items(), key=lambda item: item[1], reverse=True))
    betweenness = list(sortedbetweeness.items())[:3]
    betweenness2 = []
    for l in betweenness:
        betweenness2.append(l[0])
    result = {'most_connected_by_num': numlist2,'most_connected_by_weight': weightlist2,'most_central_by_betweenness': betweenness2 }
    jsonobj = json.dumps(result,indent=4)
    path1 = Path(outputfile)
    if (os.path.isdir(path1.parent) == False):
        os.mkdir(path1.parent)
    with open(outputfile, 'w') as f:
        f.write(jsonobj)


if __name__ == '__main__':
    main()
