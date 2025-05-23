# -*- coding: utf-8 -*-
"""BI-Chapter1 - ORI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ol5TzZxE_zv6AhEiO8vwdnRJQbIDOqaH
"""

import pandas as pd

"""###Genomes

"""

###Vibriocholerae genome
vbgene = 'ATCAATGATCAACGTAAGCTTCTAAGCATGATCAAGGTGCTCACACAGTTTATCCACAACCTGAGTGGATGACATCAAGATAGGTCGTTGTATCTCCTTCCTCTCGTACTCTCATGACCACGGAAAGATGATCAAGAGAGGATGATTTCTTGGCCATATCGCAATGAATACTTGTGACTTGTGCTTCCAATTGACATCTTCAGCGCCATATTGCGCTGGCCAAGGTGACGGAGCGGGATTACGAAAGCATGATCATGGCTGTTGTTCTGTTTATCTTGTTTTGACTGAGACTTGTTAGGATAGACGGTTTTTCATCACTGACTAGCCAAAGCCTTACTCTGCCTGACATCGACCGTAAATTGATAATGAATTTACATGCTTCCGCGACGATTTACCTCTTGATCATCGATCCGATTGAAGATCTTCAATTGTTAATTCTCTTGCCTCGACTCATAGCCATGATGAGCTCTTGATCATGTTTCCTTAACCCTCTATTTTTTACGGAAGAATGATCAAGCTGCTGCTCTTGATCATCGTTTC'

###Ecoli genome
e = open('ecoli.txt','r')
ecoli = e.readlines()

"""#ORI and Genome replication in bacteria



Gene therapy - ensure that the genetic manipulations that they perform do not affect the origin of replication.


The initiation of replication is mediated by DnaA, a protein that binds to a short segment within the ori known as a DnaA box.

k-mer - patterncount, most frequent kmer, all frequent kmers

Frequency map

clumps - repeated motif closesly located to each other in the genome

skew(genome) - the difference between the total number of occurrences of G and the total number of occurrences of C in the first i nucleotides of Genome.
The skew diagram is defined by plotting Skewi (Genome) (as i ranges from 0 to |Genome|), where Skew0 (Genome) is set equal to zero.

Hamming distance - imperfect alignment of sequences - number of mismatches between two strings

##Pattern count
"""

#pattern count

def patterncount(string, pattern):
  k = len(pattern)
  l = len(string)
  count = 0
  for i in range(l-k+1):
    if string[i:i+k] == pattern:
      count += 1
  return count

"""##Frequency map, most frequent pattern, all most frequent patterns, pattern postitions"""

#frequency map
def freqmap(s,k):
  kmerdic = {}
  l = len(s)
  for i in range(l-k+1):
    kmerdic[s[i:i+k]] = patterncount(s,s[i:i+k])
  return kmerdic

#most frequent pattern
def mfp(s,k):
  d = freqmap(s,k)
  m = max(d.values())
  l = []
  for i in d:
    if d[i] == m:
      l.append(i)
  return l

#all mfp
def amfp(s):
  md = {}
  for i in range(1,10):
    mfpi = mfp(s,i)
    md[i] = mfpi
  return md

#pattern position in genome
def ppos(pattern, g):
  l = len(g)
  k = len(pattern)
  plist = []
  for i in range(0,l-k+1):
    if g[i:i+k] == pattern:
      plist.append(i)
  return(plist)

ppos('ATAT', 'GATATATGCATATACTT')

"""##Replication"""

#Complement
def complement(s):
  cs = ''
  for i in s.lower():
    if i == 'a':
      cs = cs+ 't'
    if i == 't':
      cs = cs+ 'a'
    if i == 'g':
      cs = cs+ 'c'
    if i == 'c':
      cs = cs+ 'g'
  return cs

#reverse complement
def rcomplement(s):
  c = complement(s)
  r = c[::-1]
  return r

s = 'CTTGATCAT'
print(complement(s))
print(rcomplement(s))

"""##clumps"""

#find clumps across the genome
#k - kmer length
#l - smaller window length
#t - cutoff
def findclumps(string, k, lt, t):
  l = len(string)
  clump = []
  for i in range(0,l-k+1):
    print('q')
    print (i)
    window = string[i,i+lt]
    print (window)
    fmap = freqmap(window,k)
    for key in fmap:
      if fmap[key] >= t:
        if fmap[key] not in clump:
          clump.append(key)
  return (clump)

findclumps(ecoli,9,500,3)

"""##skew - (g-c)"""

#skew of genome
def skew(s, i):
  cc = 0
  gc = 0
  s=s.lower()
  for k in s[:i]:
    if k == 'c':
      cc+=1
    if k == 'g':
      gc+=1
  return (abs(gc-cc))

def skewmap(s, ir):
  l = []
  for i in range(ir):
    l.append(skew(s,i))
  return l

g = 'GAGCCACCGCGATA'
skewmap(g,14)

"""##Hamming distance"""

#hamming distance - number of mismatches between two strings
def hamd(s1,s2):
  l = len(s1)
  l2 = len(s2)
  hd = 0
  if l == l2:
    for i in range(l):
      if s1[i] != s2[i]:
        hd += 1
  return hd

s = 'GGGCCGTTGGT'
k = 'GGACCGTTGAC'
hamd(s,k)

"""##App pattern matching
Find all approximate occurrences of a pattern in a string.
 Input: Strings Pattern and Text along with an integer d.
 Output: All starting positions where Pattern appears as a substring of Text with at most d mismatches.
"""

#Approximate pattern matching

def apm(pattern, s, d):
  l = len(s)
  k = len(pattern)
  spos = []
  for i in range(l-k+1):
    st = s[i:i+k]
    if hamd(st,pattern)<=d:
      spos.append(i)
  return spos

p = 'ATTCTGGA'
s = 'CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT'
apm(p,s,3)
#apc(p,s,3)

p = 'GAGG'
s = 'TTTAGAGCCTTCAGAGG'
apm(p,s,2)
apc(p,s,2)

#Approximate pattern count
def apc(pattern, s, d):
  return len(apm(pattern,s,d))