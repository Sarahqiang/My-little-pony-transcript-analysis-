import argparse
from pathlib import Path
import pandas as pd
import os, sys
import json
from pathlib import Path


def create_newlist(list1, list2, list3):
    for i in list1:
        if i not in list2:
            list3.append(i)


def check_alpha(list1, list2):
    for i in list1:
        if i.isalpha():
            list2.append(i)


def create_dict(list1, dict):
    for i in list1:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1
def get_dict(file):
    dialog = pd.read_csv(file)
    # print(len(dialog))
    tscheck = dialog['pony'].str.contains('^twilight sparkle$', na=False, case=False)
    ajcheck = dialog['pony'].str.contains('^applejack$', na=False, case=False)
    rarcheck = dialog['pony'].str.contains('^rarity$', na=False, case=False)
    ppcheck = dialog['pony'].str.contains('^pinkie pie$', na=False, case=False)
    rdcheck = dialog['pony'].str.contains('^rainbow dash$', na=False, case=False)
    fscheck = dialog['pony'].str.contains('^fluttershy$', na=False, case=False)
    dialog = dialog[(tscheck) | (ajcheck) | (rarcheck) | (ppcheck) | (rdcheck) | (fscheck)]
    dialog = dialog.drop('title', 1)
    dialog = dialog.drop('writer', 1)
    dialog['dialog'] = dialog['dialog'].str.replace('(', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace(')', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace('[', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace(']', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace(',', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace('-', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace('.', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace('?', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace('!', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace(':', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace(';', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace('#', ' ')
    dialog['dialog'] = dialog['dialog'].str.replace('&', ' ')
    dialog['dialog'] = dialog['dialog'].str.lower()
    dialog['pony'] = dialog['pony'].str.lower()
    # dialog = dialog[~dialog.dialog.isin(dialog.dialog.value_counts().loc[lambda x: x < 5].index)]
    dialog['list'] = dialog['dialog'].str.split().tolist()
    # print(dialog)
    ts = dialog.groupby(['pony']).get_group("twilight sparkle")['list'].tolist()
    tslist = [i for j in ts for i in j]
    aj = dialog.groupby(['pony']).get_group("applejack")['list'].tolist()
    ajlist = [i for j in aj for i in j]
    rar = dialog.groupby(['pony']).get_group("rarity")['list'].tolist()
    rarlist = [i for j in rar for i in j]
    pp = dialog.groupby(['pony']).get_group("pinkie pie")['list'].tolist()
    pplist = [i for j in pp for i in j]
    rd = dialog.groupby(['pony']).get_group("rainbow dash")['list'].tolist()
    rdlist = [i for j in rd for i in j]
    fs = dialog.groupby(['pony']).get_group("fluttershy")['list'].tolist()
    fslist = [i for j in fs for i in j]
    # with open("/Users/yaoqiangwu/Desktop/hw8/submission_template/data/stopwords.txt", 'r') as f:
    #   a = f.read().splitlines()
    #   charlist = a[6:]
    charlist = ['a', 'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along',
                'already', 'also',
                'although', 'always', 'among', 'an', 'and', 'another', 'any', 'anybody',
                'anyone', 'anything', 'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking',
                'asks', 'at',
                'away', 'b', 'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes',
                'been',
                'before', 'began', 'behind', 'being', 'beings', 'best', 'better', 'between', 'big', 'both', 'but', 'by',
                'c',
                'came', 'can', 'cannot', 'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could',
                'd', 'did',
                'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'down', 'downed', 'downing',
                'downs', 'during',
                'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even', 'evenly', 'ever',
                'every',
                'everybody', 'everyone', 'everything', 'everywhere', 'f', 'face', 'faces', 'fact', 'facts', 'far',
                'felt', 'few',
                'find', 'finds', 'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered', 'furthering',
                'furthers',
                'g', 'gave', 'general', 'generally', 'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good',
                'goods',
                'got', 'great', 'greater', 'greatest', 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has',
                'have',
                'having', 'he', 'her', 'here', 'herself', 'high', 'high', 'high', 'higher', 'highest', 'him', 'himself',
                'his',
                'how', 'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 'interesting', 'interests',
                'into', 'is',
                'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows', 'l',
                'large',
                'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely', 'long',
                'longer',
                'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men',
                'might', 'more',
                'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed',
                'needing',
                'needs', 'never', 'new', 'new', 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not',
                'nothing', 'now',
                'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 'older', 'oldest',
                'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered', 'ordering',
                'orders',
                'other', 'others', 'our', 'out', 'over', 'p', 'part', 'parted', 'parting',
                'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 'possible',
                'present',
                'presented', 'presenting', 'presents', 'problem', 'problems', 'put', 'puts', 'q', 'quite', 'r',
                'rather', 'really',
                'right', 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says', 'second', 'seconds',
                'see', 'seem',
                'seemed', 'seeming', 'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing',
                'shows',
                'side', 'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone',
                'something',
                'somewhere', 'state', 'states', 'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that',
                'the',
                'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things', 'think', 'thinks',
                'this',
                'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today', 'together', 'too',
                'took',
                'toward', 'turn', 'turned', 'turning', 'turns', 'two',
                'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted',
                'wanting',
                'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'when', 'where',
                'whether', 'which',
                'while', 'who', 'whole', 'whose', 'why', 'will', 'with',
                'within', 'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years',
                'yet', 'you', 'young', 'younger', 'youngest', 'your', 'yours', 'z']

    tslist2, ajlist2, rarlist2, pplist2, rdlist2, fslist2 = [], [], [], [], [], []
    create_newlist(tslist, charlist, tslist2)
    create_newlist(ajlist, charlist, ajlist2)
    create_newlist(rarlist, charlist, rarlist2)
    create_newlist(pplist, charlist, pplist2)
    create_newlist(rdlist, charlist, rdlist2)
    create_newlist(fslist, charlist, fslist2)
    allword = tslist2 + ajlist2 + rarlist2 + pplist2 + rdlist2 + fslist2
    wordlessthan5 = []
    for i in allword:
        if allword.count(i) < 5:
            wordlessthan5.append(i)
    tslist3, ajlist3, rarlist3, pplist3, rdlist3, fslist3 = [], [], [], [], [], []
    create_newlist(tslist2, wordlessthan5, tslist3)
    create_newlist(ajlist2, wordlessthan5, ajlist3)
    create_newlist(rarlist2, wordlessthan5, rarlist3)
    create_newlist(pplist2, wordlessthan5, pplist3)
    create_newlist(rdlist2, wordlessthan5, rdlist3)
    create_newlist(fslist2, wordlessthan5, fslist3)
    tslist4, ajlist4, rarlist4, pplist4, rdlist4, fslist4 = [], [], [], [], [], []
    check_alpha(tslist3, tslist4)
    check_alpha(ajlist3, ajlist4)
    check_alpha(rarlist3, rarlist4)
    check_alpha(pplist3, pplist4)
    check_alpha(rdlist3, rdlist4)
    check_alpha(fslist3, fslist4)
    tsdict, ajdict, rardict, ppdict, rddict, fsdict = {}, {}, {}, {}, {}, {}
    create_dict(tslist4, tsdict)
    create_dict(ajlist4, ajdict)
    create_dict(rarlist4, rardict)
    create_dict(pplist4, ppdict)
    create_dict(rdlist4, rddict)
    create_dict(fslist4, fsdict)

    finaldict = {"twilight sparkle": tsdict, "applejack": ajdict, "rarity": rardict, "pinkie pie": ppdict,
                 "rainbow dash": rddict, "fluttershy": fsdict}

    return finaldict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    clean_dialog = f'{args.input}'
    outputfile = f'{args.output}'
    path = Path(outputfile)
    if (os.path.isdir(path.parent) == False):
        os.mkdir(path.parent)
    path.parent.absolute()
    finaldict = get_dict(clean_dialog)
    json_object = json.dumps(finaldict, indent=4)
    with open(outputfile, 'w') as json_file:
        json_file.write(json_object)
    # print(tslist4)
    # print(len(tslist), len(ajlist), len(rarlist), len(pplist), len(rdlist), len(fslist))
    # print(len(tslist2),len(ajlist2),len(rarlist2),len(pplist2),len(rdlist2),len(fslist2))
    # print(len(tslist3), len(ajlist3), len(rarlist3), len(pplist3), len(rdlist3), len(fslist3))


if __name__ == '__main__':
    main()
