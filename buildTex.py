# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:59:24 2020

@author: tom
"""

import yaml
import unidecode

with open('members.yaml', 'r') as stream:
    try:
        dic = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

members = []
affiliations = []

for author in list(dic['PIs'].keys()):
    for i, name in enumerate(author.split()[::-1]):
        if i == 0:
            aut = [name]
        else:
            aut.append(name[0])
    members.append('. '.join(aut[::-1]))
    affiliations.append(dic['PIs'][author]['Affiliation'])

membersTemp = []
membersToSort = []
affiliationsTemp = []

for member in list(dic['Members'].keys()):
    for i, name in enumerate(member.split()[::-1]):
        if i == 0:
            mem = [name]
        else:
            mem.append(name[0])
    membersTemp.append('. '.join(mem[::-1]))
    mem = [unidecode.unidecode(name.lower()) for name in mem]
    membersToSort.append(' '.join([mem[0]] + mem[1:][::-1]))
    affiliationsTemp.append(dic['Members'][member]['Affiliation'])

idxs = sorted(range(len(membersToSort)), key=membersToSort.__getitem__)

membersTemp = [membersTemp[i] for i in idxs]
affiliationsTemp = [affiliationsTemp[i] for i in idxs]

members += membersTemp
affiliations += affiliationsTemp

affilUniq = []
affilIDs = []

for affil in affiliations:
    if type(affil) == list:
        ID = []
        for aff in affil:
            if aff not in affilUniq:
                affilUniq.append(aff)
            ID.append(str(affilUniq.index(aff) + 1))
        affilIDs.append(', '.join(ID))
    else:
        if affil not in affilUniq:
            affilUniq.append(affil)
        affilIDs.append(str(affilUniq.index(affil) + 1))

member_block = ''

if len(members) < 3:
    if len(members) == 1:
        member_block += '\\mbox{' + members[0].replace(' ', '~')
        member_block += '\\textsuperscript{' + affilIDs[0] + '}}'
    elif len(members) == 2:
        member_block += '\\mbox{' + members[0].replace(' ', '~')
        member_block += '\\textsuperscript{' + affilIDs[0] + '}} '
        member_block += 'and \\mbox{' + members[1].replace(' ', '~')
        member_block += '\\textsuperscript{' + affilIDs[1] + '}}'
else:
    len_members = len(members) - 1
    for i, member in enumerate(members):
        if i < len_members:
            member_block += '\\mbox{' + member.replace(' ', '~')
            member_block += ',\\textsuperscript{' + affilIDs[i] + '}} '
        if i == len_members:
            member_block += 'and \\mbox{' + member.replace(' ', '~')
            member_block += '\\textsuperscript{' + affilIDs[i] + '}}'

affil_block = ''

len_affils = len(affilUniq) - 1

for i, affil in enumerate(affilUniq):
    if i < len_affils:
        affil_block += '\\textsuperscript{' + str(i + 1) + '}'
        affil_block += affil + '\\\\ '
    else:
        affil_block += '\\textsuperscript{' + str(i + 1) + '}' + affil

affil_block = affil_block.replace('&', r'\&')
affil_block = affil_block.replace('\\\\ ', '}\\\\ \\mbox{')
affil_block = affil_block.replace(', ', '}, \\mbox{')
affil_block += '}'
affil_block = '\\mbox{' + affil_block

with open('template.tex.txt', 'r') as f:
    template = f.read()

template = template.replace('{% MEMBER BLOCK %}', member_block)
template = template.replace('{% AFFIL BLOCK %}', affil_block)

with open('member_list.tex', 'w') as f:
    f.write(template)
