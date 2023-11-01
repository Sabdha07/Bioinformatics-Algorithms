# -*- coding: utf-8 -*-
"""BIOINFO-Chapter2-motiffind.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XGrzT4gPEShpFREY7jBhRdMTU81vp92_

##Motifs
"""

def lower_case(m):
  nm = []
  for i in m:
    nm.append(i.lower())
  return nm

m = ['AACGTA','CCCGTT', 'CACCTT','GGATTA','TTCCGG']

example_motifs = lower_case(m)

"""##Frequent words problem"""

#pattern count

def pattern_count(string, pattern): #counts the number of times the pattern appears in the given string
  k = len(pattern)
  l = len(string)
  count = 0
  for i in range(l-k+1):
    if string[i:i+k] == pattern:
      count += 1
  return count

#frequency map
def frequency_map(string,k): #frequency map for all kmers in the string
  kmerdic = {}
  l = len(string)
  for i in range(l-k+1):
    kmerdic[string[i:i+k]] = pattern_count(string,string[i:i+k])
  return kmerdic

#most frequent pattern
def most_frequent_pattern(string,k): #given a string, most_frequent_pattern returns the most frequent kmer
  d = frequency_map(string,k)
  m = max(d.values())
  l = []
  for i in d:
    if d[i] == m:
      l.append(i)
  return l

def hamming_distance(p,q):
    d = 0
    if len(p) == len(q):
      for i in range(len(p)):
        if p[i] != q[i]:
          d += 1
    return d

def approximate_pattern_matching(seq, kmer, d): #approximate text matching
    flag = False
    if len(seq) == len(kmer):
      if hamming_distance(kmer,seq) <= d:
        flag = True
    return flag

#patterncount allowing d mismatches
def patterncount_with_mismatch(string,pattern,d):
  k = len(pattern)
  l = len(string)
  count = 0
  for i in range(l-k+1):
    if approximate_pattern_matching(string[i:i+k],pattern,d):
      count += 1
  return count

#frequency map with d mismatches
def frequency_map_with_dmismatch(string,k,d):
  kmerdic = {}
  l = len(string)
  for i in range(l-k+1):
    kmerdic[string[i:i+k]] = patterncount_with_mismatch(string,string[i:i+k],d)
  return kmerdic

#most frequent pattern allowing d mismatches
def most_frequent_pattern_with_dmismatch(string,k,d):
  d = frequency_map_with_dmismatch(string,k,d)
  m = max(d.values())
  l = []
  for i in d:
    if d[i] == m:
      l.append(i)
  return l

"""##Motif enumeration"""

from itertools import product

def all_patterns_with_dmismatch(pattern, d):
    nucleotides = 'acgt'
    npatterns = []
    k = len(pattern)
    comb = list(product(nucleotides, repeat=k))
    n = ''
    alist = []
    for i in comb:
      n  = ''.join(i)
      alist.append(n)
    for kmern in alist:
      if hamming_distance(kmern,pattern) <= d:
        npatterns.append(kmern)
    return set(npatterns)

def present_in_allseq(dna,pattern,d):
  n = len(dna)
  k = len(pattern)
  c = 0
  for seq in dna:
    for i in range(len(seq)-k+1):
      kmer = seq[i:i+k]
      if hamming_distance(kmer,pattern) <= d:
        c += 1
        break
  if c == n:
    return True
  else:
    return False

def MotifEnumeration(dna, k, d):
    patterns = []
    for seq in range(len(dna)):
      for i in range(len(dna[0]) - k + 1):
          kmer = dna[seq][i:i+k]
          npattern = all_patterns_with_dmismatch(kmer, d)
          for pat in npattern:
            if present_in_allseq(dna,pat,d):
              patterns.append(pat)
    return set(patterns)

dnamotifenumeration = lower_case(['ATTTGGC', 'TGCCTTA', 'CGGTATC', 'GAAAATT'])
MotifEnumeration(dnamotifenumeration,3,1)

"""##Scoring of motif matrices

"""

#Motif matrix scoring
def motifcount(motifs):
  c = {}
  l = len(motifs[0])
  for i in 'acgt':
    c[i] = []
    for j in range(l):
      c[i].append(0)
  t = len(motifs)
  for i in range(t):
      for j in range(l):
        symbol = (motifs[i][j]).lower()
        c[symbol][j] += 1
  return c

motifcount(example_motifs)

# the frequency of the i-th nucleotide in the j-th column of the motif matrix
#i.e., the number of occurrences of the i-th nucleotide divided by t, the number of nucleotides in the column
def profile(motifs):
  t = len(motifs)
  cp = motifcount(motifs)
  for i in cp:
    k = len(cp[i])
    for j in range(k):
      cp[i][j] = cp[i][j]/t
  return cp

#consensus find
def consensus(motifs):
  cp = profile(motifs)
  consensus = ''
  for j in range(len(motifs[0])):
    c = 0
    sym = ''
    for i in 'atgc':
      if cp[i][j] >= c:
        sym = i
        c = cp[i][j]
    consensus = consensus + sym
  return consensus

#motif scoring
def score(Motifs):
    s = 0
    c = consensus(Motifs)
    coln = len(Motifs[0])
    rown = len(Motifs)
    for i in range(rown):
      for j in range(coln):
        if Motifs[i][j] != c[j]:
          s += 1
    return s

#Probability of a seq given profile:
def Pr(s, pr):
    # insert your code here
    p = 1
    for i in range(len(s)):
        sym = s[i]
        prob = pr[sym][i]
        p = p*prob
    return p

#Entropy of motifs given profile:
import math as m
def ls(x):
  if x ==0:
    return 0
  y = -1*x* m.log(x,2)
  return y

def entropy(motif, pr):
  es = 0
  n = len(motif)
  l = len(motif[0])
  for i in range(n):
    for j in range(l):
      sym = motif[i][j]
      es += ls(pr[sym][j])
  return es

"""##Greedy motif search"""

#profile most probable kmer
def pmpk(string,k,profile):
  l = len(string)
  p=0
  pkmer = string[0:k]
  for i in range(l-k+1):
    kmer = string[i:i+k]
    pr = Pr(kmer,profile)
    if pr > p:
      p = pr
      pkmer = kmer
  return pkmer

#Greedy motif search
def GreedyMotifSearch(dna,k,t):
  mot = []
  l = len(dna[0])
  for seq in dna:
    mot.append(seq[0:k])
  bestmotifs = mot

  for i in range(l-k+1):
    motifs = []
    kmer = dna[0][i:i+k]
    motifs.append(kmer)
    for j in range(1,t):
      p = profile(motifs)
      nextmotif = pmpk(dna[j],k,p)
      motifs.append(nextmotif)
    if score(motifs) < score(bestmotifs):
      bestmotifs = motifs
  return bestmotifs

Dna =lower_case(["GGCGTTCAGGCA","AAGAATCAGTCA","CAAGGAGTTCGC","CACGTCAATCAC","CAATAATATTCG"])

print(GreedyMotifSearch(Dna,3,5))

dnag =lower_case(['TTAGAGAGCGAATCAATTCAGACTGAGAAAACGATCGAACGTCGCGAGCGAAAAGAGCCCTGAACAAATGTGCTGGCAAGGCTCATCCTGCAGGGTGTGCATTGAGGGACGCATGCGATGTTATGACATGTTCAAGTCAGCGGGCGTACTTCAAAC',
'CAGCAGACGATCATCCTACAACTCCTTGCGTTCATATGAGGAACTGCACGAGAGGTTAGAGTCACAGGATTCATATTGCTCTTCATTTCCGGTCGGGTACAAACGGTAGTTAGGTTACTCCTAGTTAGATACGAGTGGATAATAAGTTGGCACGGT',
'CCCGTTGCATCACACCAACGCCTAGGATATGGCCATCTTTGCTGATCCCTCGTGACACTTTAGTCACCGTTGGTGGCTAGAATCTAAATCACGAAGTGGGCTTATATGCAGCGAGGCGATACCTCCTAAACAGAGTAAACTATCACACACTACTGG',
'GCACCCTCCCCATCTGTCGACGCGGAGCAGACCATCTGGTCGAGCACAATCCCAGCCGGTGGCAACTTTTTGAGCCACGATCTTTAGGGACACCAGGGTGGGCTTCCCGTCATCTATGCTGACCCCGGAGGATCGCAACGCCAGTCCGTAGTGCAT',
'TATCTAATCCCTGAGCACAGTACACTGAGCTATCAGCGAAAAGTTAATTTTGCGAGTTGGGAGTATACGATCGATAAGGCTCTTTCCTGAATCACGTGGACTCGGAAAGTCCGGTTCGTGCCATTGGCACCTAAGTCAGGGGCCTGCAGTGTGTTG',
'TCTCTCTACGCGCAGGTGGTTTTTTGTGTTGGCGCCAAAGTCATACATGCGGTCTGGATTTCTACGGGAGCTAGTGGTGATGCCCAGCCATCGCCTTCGACGTTCTAGAAGAACACCATCCTTCGTGAATCATGGATTATATACGCTTAAGGCTTC',
'CTTCTGTATTTCACACATGAGCGAGGAAGCAGTGAGTCCGAACAGCAGCTGGACGGCCATACCTAAGCTCGGTGGAGTTGAAGCGTAGTACGAGTGCCCCTGTCCGCACAAGGTAAATTTAAAGTTTGGGGCTACCCGGATACCAAGTAAACCATC',
'CGAGTATGCATGGAAGCGTCCAGGGTACGCAATGCTGACAAGGGTGGTGAGTGTCAGAGTGAGAACACGATCTAGTGGGTGAGAGTCGACCCCCCGTCTGAGCCTACTGATGGCGGGTATGCGTGTCGTGGTGCATATTCCCCATATTCGATTGGC',
'AACGACTGGTGTATCCCCAGCGGTAAATGCGGTAGTGGACGTGATCCATAGTAGACTATCCATGGAGAAAACGCTACTCATTTGGTGATTTAACAAGAGTAGCGGGCCACCCCCATTGTCGTGGACGGGACACAGAGGTACGACAAATGCCCGTGT',
'GACTCACCTACGCGTGTCCATAAGGGAACAGTACAATTCCGATTCAGGTAGGCGAAATCGAAGTTTCGTAGATTGCCTATGCGGTTTTGCCCTTCCCAGGAGACGATCCTTGCTGTGATTTGGTACGTAAGAAAGAATCCGCGTCTGGGGAGACTG',
'TGTTAATACTGTAGCGTTGTTGCAGCTGGCGACTACTTCTGCGTGGCTAAGGAGTCTTATAGCAAGCCTCTGGACATGGGTGATCATGACTCTTATCGGTCACTTTCCCAGTAGACCATCGACCGGCGGATGGAAGTTGCGAGAGTTACTCTAATT',
'TAATACAGTATGACGTGCCCGATGGAGCATACTATCATTTTTTATTTAAGCCCTATAGGGACTACACTACACCAGGAACGTAAATCACTCGGGCGTGATGACTAACTGATTGCAGTTGAGGTCGGCATCGGCTTTGGCCATCATGTGAAAATACAT',
'GCGAAATTGGCGCAGGAACTGCAGTGGTCCAGGGGTATACGTATTCGACCTGCACGCCAGGACAGCCGTGTCGAGGCCGAGCGCTCGAGCGGTAGACAGAACACAATCCGATGGAACGGGGTCTAGTGCGTGAGCAAAACCATCCAGACTATGTTA',
'GACCACTTGTGGACTATTAGGAATTAGAAGACAATCAGCCCCTTGACCCGCCCTTTAAGAAGACTTGAACCTTTTTACCCCATGTAAATATAGCGGAATCGGTAGAGAGATCGATTTCAGTCATCCCATCCGGACACTTTGAAAGACCCCAACGTA',
'GGAATATCTTCCTGCAGAGCCTTTAGAATCGTCGACAAGGGACTTTTATAGGCGGAACGAAGCCGCAAGGGGAAATGGCTCCGGCAGCATACCATCTGTAAAGTTGACGAGAAAAGTATTAAAATTCGGACCTGGACAGTATCTGTTCCCCGGCCT',
'TTTCCGAGCACCGTGCGGGCGGAAACGCCTTGGCATGGAGAGTGCACAGTCAGCACCTAATGGTCGGGGGCCGATGTTGGTAGGATTGGTACAGCTCTCTGCATGCGCACGCCACCACTGCCGCAGTATAGAGAGGAAACCATCAAGTTCATGTGC',
'TTAGCCAACAGGGCAAGACATCCCGTCCCTCTTGATTTTTCCGTCACCAAGTCAGTTAGTGGTCCACACAAAGTTCAGCTTCGAAAGCAAACAATCGAAACAAATAAACACTGATGAAGTGATCATTAATTGCTAATAATGCTAAACACCAATGCT',
'GTTAGGAAGGGCTGATGTCTTGAGAGTCCGTTCCGACAGTACACAATCGACTTTAGATCAAGTTCAAGTAAACGAGAGTTCCCGCCGCAATGTTCTCTTGGCTGGGTAGGCATCATCGTCCCGTCTTGGTCTGCATGTGGCGATCGTTACAAATCT',
'AGTGGCCGCCCGGGACAAGGCAGTCTAATCTTTTGTTGAAAGACCATCTCTTTGCGCCAGTCAGGCAACGTATTTACAGCAGACGTGCGGGGCATCTGAATTCTCAACAGGCGGTGACACGATCCAAAGCACAAGGACACTATCGATTACTTAGTC',
'GACGCAGGGGTCCTACATCAGACGATTCTTAACACGCTATGGTGTCATTTATATAGGTTCCAGGAAACTATCGAACAGGTTTTAATAACGTCTCTGCAGTCCTTGATAGTCGATCCTAAATCTGCGTAAAACTGTTTAGCATTCGAATGCTGAGCC',
'TCGGTGCCTAGTGCGGATGTGCAACGCTCGCGTGTCCATTTGAAGCAATTCGCTATATAGTAAGCTGATGCTAAGTATACGATCAGGCGTACTGGTCCAGCGGAGTAGATGACGAGTTAAGTGTTGCGAGTGTTATGAGCGGGGCGATAGTATCGC',
'AAGACCTCGAACGGCCATACTGTGGGATATGGGTGAGCGTGCTTTAACGCCGTCGGTCATTATGCTGGGCACTTCTACGTGAATGATTAGTGTATTCGTTAAGTAGCCGAAGATGCATGAGTACCGGTCCCCTAGCACACAATCTAGCGATCAAAG',
'GCCCAGCATCGACCGAAGCTAGTATCCCACGCTTGGAGTAGCCCTCCATTCAAACAGTTATAGGACACTATCGACAAGCGAGAACAGGAGATGCAATGCTAAGTGGGGCCCGCAGGGCTGAATAAGCGTCCCGCGACCTGCTTCCGTGATACCGGT',
'TTAGACTATCGCGGCCTCACCTGCACTTACCACTAGTAGTAAACGATCAGTGTGTCTCCGGAATTGAATGTCGCGTCGGGCTCTTTACACTGCGACCTTGCCGTAAACTCTATCCGATATCTAGCGACCTTGTCGTAAGGCGAACGTATGCTGGAG',
'TATGCGGCAAGCGAGGTAGCCACATCGAATGCAGGGCTATATGCCCCCATACGGTCTGGGCAAGATGCTTTTCTTCTCCACGTTCACCGAAAATACTTTTAGTTAACGGGCACAACTGTACAGTATACAATCAAGAACACGAAGAGTTCTCCGGTA'])
print(GreedyMotifSearch(dnag,12,25))

"""##Improved greedy search"""

#Motif matrix scoring - improved- Laplace
def countn(motifs):
  c = {}
  l = len(motifs[0])
  for i in 'acgt':
    c[i] = []
    for j in range(l):
      c[i].append(1)
  t = len(motifs)
  for i in range(t):
      for j in range(l):
        symbol = (motifs[i][j]).lower()
        c[symbol][j] += 1
  return c

def profilen(motifs):
  cp = countn(motifs)
  t = 0
  for i in cp:
    t += cp[i][0]
  for i in cp:
    k = len(cp[i])
    for j in range(k):
      cp[i][j] = cp[i][j]/t
  return cp

def consensusn(motifs):
  cp = profilen(motifs)
  consensus = ''
  for j in range(len(motifs[0])):
    c = 0
    sym = ''
    for i in 'atgc':
      if cp[i][j] >= c:
        sym = i
        c = cp[i][j]
    consensus = consensus + sym
  return consensus

def scoren(Motifs):
    s = 0
    c = consensusn(Motifs)
    coln = len(Motifs[0])
    rown = len(Motifs)
    for i in range(rown):
      for j in range(coln):
        if Motifs[i][j] != c[j]:
          s += 1
    return s

def ImprovedGreedyMotifSearch(dna,k,t): #Laplace's succession rule
  mot = []
  l = len(dna[0])
  for seq in dna:
    mot.append(seq[0:k])
  bestmotifs = mot

  for i in range(l-k+1):
    motifs = []
    kmer = dna[0][i:i+k]
    motifs.append(kmer)
    for j in range(1,t):
      p = profilen(motifs)
      nextmotif = pmpk(dna[j],k,p)
      motifs.append(nextmotif)
    if scoren(motifs) < scoren(bestmotifs):
      bestmotifs = motifs
  return bestmotifs,scoren(motifs)

print(GreedyMotifSearch(['atgcg','tattc','agagc','ttcca'],3,4))
print(ImprovedGreedyMotifSearch(['atgcg','tattc','agagc','ttcca'],3,4))

"""##Median String Problem"""

#hamming distance between two strings of same length
def hd(s,t):
  l = len(s)
  hd = 0
  if l == len(t):
    for i in range(l):
      if s[i]!=t[i]:
        hd+=1
    return hd

#hamming distance between pattern and text
def ds(pattern, text):
  k = len(pattern)
  l = len(text)
  kl = k
  for i in range(l-k+1):
    kmer = text[i:i+k]
    if len(kmer) == len(pattern):
      if hd(kmer,pattern) < kl:
        kl = hd(kmer,pattern)
  return kl #returns minimum hd among all kmers in the text

def motif(pattern, text):
  k = len(pattern)
  l = len(text)
  kl = k
  m = ''
  for i in range(l+k-1):
    kmer = text[i:i+k]
    if len(kmer) == len(pattern):
      if hd(kmer,pattern) < kl:
        kl = hd(kmer,pattern)
        m = kmer
  return m #returns the motif with the minimum hd

#sum of mimal hd in each seq in a set of seq-dna
def d(pattern,dna):
  sum = 0
  for seq in dna:
    sum += ds(pattern,seq)
  return sum

#Median String Problem
def medstring(dna,k):
  n = len(dna)
  distance = len(dna[0])
  median = dna[0][:k]
  for seq in dna:
    for i in range(len(seq)-k+1):
      pattern = seq[i:i+k]
      if distance >= d(pattern,dna):
        distance = d(pattern,dna)
        median = pattern
  return median, distance

dna2 = lower_case(['AAATTGACGCAT', 'GACGACCACGTT', 'CGTCAGCGCCTG', 'GCTGAGCACCGG', 'AGTACGGGACAG'])
medstring(dna2,3)

dna3= lower_case(
['CTGCGCTCCGCAATCTTCATTGGTTCGGCCGTGTGAACTCCT',
'GCTCCTTCGGTGCCTTGTGCCAGACTAGAACCGCGGGCCTAC',
'AAGCACGCTGGTGTTTGCAAGATTGTCGGGCTCAGGGCTCCT',
'GAGGAATCTCCTATAGCCAACAGGACCTTTGTTATGCATCGT',
'CCTCCTGCCAGATATCCCCCAAGTTAGGAATTTGCCGCCGGG',
'CAATAGCCTCCTGTGCCAATCGTAGTCGCCATGGGGTGTACA',
'AAGAAGGGATGATGTGCCCCTCCTCGCGATAACAACTACCTT',
'CAGCACGGTCAAACTCCTAGACCACGTCATGGTTTGGGTTAC',
'ACTCCTGGACCCTCATTTATTCTGACGACAATATTGATCGGA',
'ACGTTCCTCCATATGGTGTCCTAGTTTGTGTTCAAACCTCCT'])
medstring(dna3,5)

"""##Randomized"""

import random
def randommotifs(dna,k):
  t = len(dna[0])
  l = list(range(t-k+1))
  mot = []
  for seq in dna:
    n = random.choice(l)
    kmer = seq[n:n+k]
    mot.append(kmer)
  return mot

def motif(pr,dna):
  mot = []
  k = len(pr['a'])
  for seq in dna:
    mot.append(pmpk(seq,k,pr))
  return mot

def RandomizedMotifSearch(dna,k,t):
  mot = randommotifs(dna,k)
  bmot = mot
  for i in range(1000):
    pr = profilen(mot)
    mot = motif(pr,dna)
    if scoren(mot) < scoren(bmot):
      bmot = mot
  return bmot, scoren(bmot)

p = profilen(['gtc','ccc','ata','gct'])
dna = lower_case(['ATGAGGTC','GCCCTAGA','AAATAGAT','TTGTGCTA'])
mot = motif(p,dna)
mot

dnar = lower_case(['CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA','GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG','TAGTACCGAGACCGAAAGAAGTATACAGGCGT',
'TAGATCAAGTTTCAGGTGCACGTCGGTGAACC','AATCCACCAGCTCCACGTGCAATGTTGGCCTA'])
print(RandomizedMotifSearch(dnar,8,1005))
print(RandomizedMotifSearch(dnar,8,105))
print(RandomizedMotifSearch(dnar,8,5000))

RandomizedMotifSearch(['atgcg','tatgc','agatg','ttgca'],3,4)

"""##Gibbs Sampling"""

def Random(p):
    sum = 0
    for i in p:
        sum += p[i]
    if sum != 1:
        for i in p:
            p[i] = p[i]/sum
    kmer = '' # output variable
    alp = []
    pro = []
    for i in p:
        alp.append(i)
        pro.append(p[i])
    from random import choices
    return choices(alp,pro)[0]

#profile randomly generated kmer
def prgk(string,k,profile):
  l = len(string)
  pdis = {}
  pkmer = string[0:k]
  for i in range(l-k+1):
    kmer = string[i:i+k]
    pdis[kmer] = (Pr(kmer,profile))
  return (Random(pdis))

dnapr=lower_case(['AAACCCAAACCC'])
profile = {'a': [0.5, 0.1], 'c': [0.3, 0.2], 'g': [0.2, 0.4], 't': [0.0, 0.3]}
print(prgk(dnapr[0],2,profile))

from random import randint
def GibbsSampler(dna,k,t,N):
  moti = randommotifs(dna,k)
  mot = moti
  bestmot = moti.copy()
  for j in range(0,N):
    i = randint(0,t-1)
    newmotif = []
    for m in range(t):
      if m!=i:
        newmotif.append(mot[m])
    prof = profilen(newmotif)
    motifi = prgk(dna[i],k,prof)
    mot[i] = motifi
    if scoren(mot) < scoren(bestmot):
      bestmot = mot
  return bestmot,scoren(bestmot)

gdna = lower_case(['CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA',
'GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG',
'TAGTACCGAGACCGAAAGAAGTATACAGGCGT',
'TAGATCAAGTTTCAGGTGCACGTCGGTGAACC',
'AATCCACCAGCTCCACGTGCAATGTTGGCCTA'])
print(GibbsSampler(gdna,8,5,1000))
print(GibbsSamp(gdna,8,5,1000))
print(GibbsSampN(gdna,8,5,1000))

"""##DosR - TB"""

dnatb =lower_case(['GCGCCCCGCCCGGACAGCCATGCGCTAACCCTGGCTTCGATGGCGCCGGCTCAGTTAGGGCCGGAAGTCCCCAATGTGGCAGACCTTTCGCCCCTGGCGGACGAATGACCCCAGTGGCCGGGACTTCAGGCCCTATCGGAGGGCTCCGGCGCGGTGGTCGGATTTGTCTGTGGAGGTTACACCCCAATCGCAAGGATGCATTATGACCAGCGAGCTGAGCCTGGTCGCCACTGGAAAGGGGAGCAACATC',
'CCGATCGGCATCACTATCGGTCCTGCGGCCGCCCATAGCGCTATATCCGGCTGGTGAAATCAATTGACAACCTTCGACTTTGAGGTGGCCTACGGCGAGGACAAGCCAGGCAAGCCAGCTGCCTCAACGCGCGCCAGTACGGGTCCATCGACCCGCGGCCCACGGGTCAAACGACCCTAGTGTTCGCTACGACGTGGTCGTACCTTCGGCAGCAGATCAGCAATAGCACCCCGACTCGAGGAGGATCCCG',
'ACCGTCGATGTGCCCGGTCGCGCCGCGTCCACCTCGGTCATCGACCCCACGATGAGGACGCCATCGGCCGCGACCAAGCCCCGTGAAACTCTGACGGCGTGCTGGCCGGGCTGCGGCACCTGATCACCTTAGGGCACTTGGGCCACCACAACGGGCCGCCGGTCTCGACAGTGGCCACCACCACACAGGTGACTTCCGGCGGGACGTAAGTCCCTAACGCGTCGTTCCGCACGCGGTTAGCTTTGCTGCC',
'GGGTCAGGTATATTTATCGCACACTTGGGCACATGACACACAAGCGCCAGAATCCCGGACCGAACCGAGCACCGTGGGTGGGCAGCCTCCATACAGCGATGACCTGATCGATCATCGGCCAGGGCGCCGGGCTTCCAACCGTGGCCGTCTCAGTACCCAGCCTCATTGACCCTTCGACGCATCCACTGCGCGTAAGTCGGCTCAACCCTTTCAAACCGCTGGATTACCGACCGCAGAAAGGGGGCAGGAC',
'GTAGGTCAAACCGGGTGTACATACCCGCTCAATCGCCCAGCACTTCGGGCAGATCACCGGGTTTCCCCGGTATCACCAATACTGCCACCAAACACAGCAGGCGGGAAGGGGCGAAAGTCCCTTATCCGACAATAAAACTTCGCTTGTTCGACGCCCGGTTCACCCGATATGCACGGCGCCCAGCCATTCGTGACCGACGTCCCCAGCCCCAAGGCCGAACGACCCTAGGAGCCACGAGCAATTCACAGCG',
'CCGCTGGCGACGCTGTTCGCCGGCAGCGTGCGTGACGACTTCGAGCTGCCCGACTACACCTGGTGACCACCGCCGACGGGCACCTCTCCGCCAGGTAGGCACGGTTTGTCGCCGGCAATGTGACCTTTGGGCGCGGTCTTGAGGACCTTCGGCCCCACCCACGAGGCCGCCGCCGGCCGATCGTATGACGTGCAATGTACGCCATAGGGTGCGTGTTACGGCGATTACCTGAAGGCGGCGGTGGTCCGGA',
'GGCCAACTGCACCGCGCTCTTGATGACATCGGTGGTCACCATGGTGTCCGGCATGATCAACCTCCGCTGTTCGATATCACCCCGATCTTTCTGAACGGCGGTTGGCAGACAACAGGGTCAATGGTCCCCAAGTGGATCACCGACGGGCGCGGACAAATGGCCCGCGCTTCGGGGACTTCTGTCCCTAGCCCTGGCCACGATGGGCTGGTCGGATCAAAGGCATCCGTTTCCATCGATTAGGAGGCATCAA',
'GTACATGTCCAGAGCGAGCCTCAGCTTCTGCGCAGCGACGGAAACTGCCACACTCAAAGCCTACTGGGCGCACGTGTGGCAACGAGTCGATCCACACGAAATGCCGCCGTTGGGCCGCGGACTAGCCGAATTTTCCGGGTGGTGACACAGCCCACATTTGGCATGGGACTTTCGGCCCTGTCCGCGTCCGTGTCGGCCAGACAAGCTTTGGGCATTGGCCACAATCGGGCCACAATCGAAAGCCGAGCAG',
'GGCAGCTGTCGGCAACTGTAAGCCATTTCTGGGACTTTGCTGTGAAAAGCTGGGCGATGGTTGTGGACCTGGACGAGCCACCCGTGCGATAGGTGAGATTCATTCTCGCCCTGACGGGTTGCGTCTGTCATCGGTCGATAAGGACTAACGGCCCTCAGGTGGGGACCAACGCCCCTGGGAGATAGCGGTCCCCGCCAGTAACGTACCGCTGAACCGACGGGATGTATCCGCCCCAGCGAAGGAGACGGCG',
'TCAGCACCATGACCGCCTGGCCACCAATCGCCCGTAACAAGCGGGACGTCCGCGACGACGCGTGCGCTAGCGCCGTGGCGGTGACAACGACCAGATATGGTCCGAGCACGCGGGCGAACCTCGTGTTCTGGCCTCGGCCAGTTGTGTAGAGCTCATCGCTGTCATCGAGCGATATCCGACCACTGATCCAAGTCGGGGGCTCTGGGGACCGAAGTCCCCGGGCTCGGAGCTATCGGACCTCACGATCACC'])

t = 10
N = 1000
for i in range(8,13):
  k = i
  print(k)
  print('Improved Greedy:',ImprovedGreedyMotifSearch(dnatb,k,t))
  print('Median String:', medstring(dnatb,k))
  print('Randomized:', RandomizedMotifSearch(dnatb,k,t))
  print('GibbsSampler:',GibbsSampler(dnatb,k,t,N))

"""##EDump"""

from random import randint
def GibbsSamp(dna,k,t,N):
  mot = randommotifs(dna,k)
  bmot = mot

  for j in range(0,N):
    i = randint(0,t-1)
    newmotif = mot[0:i]+mot[i+1:]
    if i == 0:
      newmotif = mot[1:]
    pr = profilen(newmotif)
    motif = prgk(dna[i],k,pr)
    mot[i] = motif
    newmotif.insert(i,motif)
    if scoren(newmotif) < scoren(bmot):
      bmot=newmotif
  return bmot, scoren(bmot)

from random import randint
def GibbsSampN(dna,k,t,N):
  for y in range(15):
    mot = randommotifs(dna,k)
    bmot = mot
    for j in range(0,N):
      i = randint(0,t-1)
      newmotif = mot[0:i]+mot[i+1:]
      if i == 0:
        newmotif = mot[1:]
      pr = profilen(newmotif)
      motif = prgk(dna[i],k,pr)
      mot[i] = motif
      newmotif.insert(i,motif)
      if scoren(newmotif) < scoren(bmot):
        bmot=newmotif



  return bmot,scoren(bmot)