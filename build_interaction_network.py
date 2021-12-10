import argparse
import json
import os, sys
from pathlib import Path

import networkx as nx
import pandas as pd


def get_chars(file):
    df = pd.read_csv(file)
    df['pony'] = df['pony'].str.lower()
    allcheck1 = df['pony'].str.contains('all ', case=False)
    allcheck2 = df['pony'].str.contains('^all$', case=False)
    allcheck3 = df['pony'].str.contains(' all', case=False)
    othercheck1 = df['pony'].str.contains('others ', na=False, case=False)
    othercheck2 = df['pony'].str.contains(' others', na=False, case=False)
    othercheck3 = df['pony'].str.contains('^others$', na=False, case=False)
    poneischeck1 = df['pony'].str.contains('^ponies$', na=False, case=False)
    poneischeck2 = df['pony'].str.contains(' ponies', na=False, case=False)
    poneischeck3 = df['pony'].str.contains('ponies ', na=False, case=False)

    andcheck1 = df['pony'].str.contains(' and ', na=False, case=False)
    andcheck2 = df['pony'].str.contains(' and', na=False, case=False)
    andcheck3 = df['pony'].str.contains('^and$', na=False, case=False)
    # andcheck1 = df['pony'].str.contains('and ', na=False, case=False)

    df = df[~othercheck1]
    df = df[~othercheck2]
    df = df[~othercheck3]
    df = df[~poneischeck1]
    df = df[~poneischeck2]
    df = df[~poneischeck3]
    df = df[~andcheck1]
    df = df[~andcheck2]
    df = df[~andcheck3]
    df = df[~allcheck1]
    df = df[~allcheck2]
    df = df[~allcheck3]

    items_count = df['pony'].value_counts().head(101).rename_axis('pony').reset_index(name='counts')
    # chars = items_counts.head(101)
    charlist = items_count['pony'].tolist()
    return charlist


def create_network(file, charlist):
    df = pd.read_csv(file)
    df = df.drop('dialog', 1)
    df = df.drop('writer', 1)
    df['pony'] = df['pony'].str.lower()
    G = nx.Graph()
    for index, row in (df.iterrows()):
        if index == 0:
            continue
        else:
            char1 = df['pony'][index - 1]
            char2 = df['pony'][index]
            char1episode = df['title'][index - 1]
            char2episode = df['title'][index]
            if char1 in charlist and char2 in charlist:
                if char1 != char2 and char1episode == char2episode:
                    if G.has_edge(char1, char2):
                        G.get_edge_data(char1, char2)['weight'] += 1
                    else:
                        G.add_edge(char1, char2)
                        G[char1][char2]['weight'] = 1
                else:
                    continue
            else:
                continue
    return G


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    clean_dialog = f'{args.input}'
    outputfile = f'{args.output}'
    inputfile = clean_dialog
    charlist = get_chars(inputfile)
    df = pd.read_csv(inputfile)
    graph = create_network(inputfile, charlist)
    result = {}
    for v in graph.nodes():
        result[v] = {}
    for v in result:
        for edge in graph.edges(v):
            result[v][edge[1]] = graph[edge[0]][edge[1]]['weight']

    jsonobj = json.dumps(result, indent=4)
    path1 = Path(outputfile)
    if (os.path.isdir(path1.parent) == False):
        os.mkdir(path1.parent)
    with open(outputfile, 'w') as f:
        f.write(jsonobj)


if __name__ == '__main__':
    main()
