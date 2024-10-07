from Bio import Phylo
import json
import sys

# tree = Phylo.read(sys.argv[1],"newick")

tree = Phylo.read("test.newick","newick")

names = tree.get_terminals()
name = []

for node in names:
    name.append(node.name)

dis = [[0 for i in range(0, len(name))] for j in range(0, len(name))]

with open("output_10.json", "r") as f:
    data = json.load(f)

qali = data["qali"]

for i in qali:
    for j in qali[i]:
        print("now",i,j)
        qali[i][j] = tree.distance(i, j)

data["qali"] = qali

with open("output_1A.json", "w") as f:
    json.dump(data, f)


# dic = {"mapping" : name,"data" : dis, "file" : sys.argv[1]}
# with open("out.json","w") as f:
#     json.dump(dic,f)