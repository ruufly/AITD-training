import json
import numpy as np

with open("ALL_FIN4_final_31genes_4098species.phy","r") as f:
    ali = f.read()

def sdf(a=np.array([[]])):
    s=np.array([])
    for i in a:
        for j in a:
            s=np.append(j)

for gw in [0,1,2,3,4,'A']:
    with open("output_3\\output_3%s.json" % gw,"r") as f:
        data = json.load(f)

    k = []
    et = []
    qali = data["qali"]

    for i in qali:
        c = []
        et.append(i)
        for j in qali[i]:
            c.append(qali[i][j])
        k.append(c)

    with open("output_3\\output_3%s_.json" % gw,"w") as f:
        json.dump(k, f)

with open("output_3\\map.json","w") as f:
    json.dump(et, f)