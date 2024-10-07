import sys, json
from Bio import Phylo

sys.setrecursionlimit(1000000)

with open("ALL_FIN4_final_31genes_4098species.phy","r") as f:
    ali = f.read()
# with open("test.newick", "r") as f:
#     tree = f.read()


# tree = Phylo.read("test.newick","newick")
# print(tree)


# ali.replace("__","_")
ali = ali.splitlines()[1:]
nali = []
qali = {}
for i in ali:
    ec = i.split()
    ec[0] = ec[0].replace("__","_")
    nali.append(ec)

print("done.1")

k = 1
c = len(nali)
for i in nali:
    print("handle[%d/%d]: %s" % (k,c,i[0]))
    k += 1
    qali[i[0]] = 0
    for j in i[1]:
        if j != "-":
            qali[i[0]]+=1

# for i in nali:
#     print("handle: %s" % i[0])
#     for j in nali:
#         distance = 0
#         for k in range(len(i[1])):
#             if i[1][k] != j[1][k]:
#                 distance += 1
#         qali[i[0]][j[0]] = distance

print("done.2")

with open("output.json","w") as f:
    json.dump(qali, f)