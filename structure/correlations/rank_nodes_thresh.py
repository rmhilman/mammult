# This file is part of MAMMULT: Metrics And Models for Multilayer Networks
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
####
##
##
## Get a file as input, whose n-th line corresponds to the value of a
## certain property of node n, and rank nodes according to their
## properties, taking into account ranking ties properly.
##
## The output is a file whose n-th line is the "ranking" of the n-th
## node according to the given property. (notice that rankings could
## be fractional, due to the tie removal algorithm)
##
## The rank of a node is set to "0" (ZERO) if the corresponding
## property is smaller than a value given as second parameter
##


import sys
import math


if len(sys.argv) < 3:
    print "Usage: %s <filein> <thresh>" % sys.argv[0]
    sys.exit(1)


thresh = float(sys.argv[2])

lines = open(sys.argv[1], "r").readlines()

ranking = []

n=0
for l in lines:
    if l[0] == "#" or l.strip(" \n").split(" ") == []:
        continue
    v = [float(x) if "." in x or "e" in x else int(x) for x in l.strip(" \n").split(" ")][0]
    if v >= thresh:
        ranking.append((v,n))
    else:
        ranking.append((0,n))
    n +=1

ranking.sort(reverse=True)
#print ranking
new_ranking = {}

v0, n0 = ranking[0]


old_value = v0
tot_rankings = 1

stack = [n0]
l=1.0
for v,n in ranking[1:]:
    l += 1
    ##print stack, tot_rankings
    if v != old_value: ### There is a new rank
        # We first compute the rank for all the nodes in the stack and then we set it
        if old_value == 0:
            new_rank_value = 0
        else:
            new_rank_value = 1.0 * tot_rankings / len(stack)
        ##print new_rank_value
        for j in stack:
            new_ranking[j] = new_rank_value
        old_value = v
        tot_rankings = l
        stack = [n]
    else: # One more value with the same rank, keep it for the future
        stack.append(n)
        tot_rankings += l

if v == 0 :
    new_rank_value = 0
else:
    new_rank_value = 1.0 * tot_rankings / len(stack)
#print new_rank_value
for j in stack:
    new_ranking[j] = new_rank_value

#print new_ranking

keys = new_ranking.keys()
keys.sort()
for k in keys:
    print new_ranking[k]
