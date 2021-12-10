import argparse
import json
import math
import os, sys


def tf(w, pony, script):
    return script[pony][w]


def idf(w, script):
    count = 0
    for key in script:
        if w in script[key]:
            count += 1
    return math.log(len(script) / count)


def tf_idf(w, pony, script):
    result = tf(w, pony, script) * idf(w, script)
    return result


def selectkey(n, d, l):
    i = 0
    keys =list(d.keys())
    for i in range(int(n)):
        l.append(keys[i])
        i += 1

def getresult(file,num):
    with open(file) as f:
        mydict = json.load(f)
        newdict = {}
    for key in mydict:
        for w in mydict[key]:
            mydict[key][w] = tf_idf(w, key, mydict)

            # newdict = sorted(newdict.items,key=lambda item: item[1],reverse=True)
    tsdict = mydict['twilight sparkle']
    sortts = dict(sorted(tsdict.items(), key=lambda item: item[1], reverse=True))
    ajdict = mydict['applejack']
    sortaj = dict(sorted(ajdict.items(), key=lambda item: item[1], reverse=True))
    rardict = mydict['rarity']
    sortrar = dict(sorted(rardict.items(), key=lambda item: item[1], reverse=True))
    ppdict = mydict['pinkie pie']
    sortpp = dict(sorted(ppdict.items(), key=lambda item: item[1], reverse=True))
    rddict = mydict['rainbow dash']
    sortrd = dict(sorted(rddict.items(), key=lambda item: item[1], reverse=True))
    fsdict = mydict['fluttershy']
    sortfs = dict(sorted(fsdict.items(), key=lambda item: item[1], reverse=True))
    tslist2, ajlist2, rarlist2, pplist2, rdlist2, fslist2 = [], [], [], [], [], []
    selectkey(num, sortts, tslist2)
    selectkey(num, sortaj, ajlist2)
    selectkey(num, sortrar, rarlist2)
    selectkey(num, sortpp, pplist2)
    selectkey(num, sortrd, rdlist2)
    selectkey(num, sortfs, fslist2)
    result = {'twilight sparkle': tslist2, 'apple jack': ajlist2, 'rarity': rarlist2, 'pinkie pie': pplist2,
              'rainbow dash': rdlist2, 'fluttershy': fslist2}
    json_object = json.dumps(result, indent=4)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--input')
    parser.add_argument('-n', '--output')
    args = parser.parse_args()
    inputfile = f'{args.input}'
    num = args.output
    print(getresult(inputfile,num))




if __name__ == '__main__':
    main()
