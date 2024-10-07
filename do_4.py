import json

a = "output_1A.json"

with open(a, "r") as f:
    data = json.load(f)

qali = data["qali"]

maxdis = -1

for i in qali:
    for j in qali[i]:
        if qali[i][j] > maxdis:
            maxdis = qali[i][j]

print(len(qali))

for i in qali:
    for j in qali[i]:
        qali[i][j] = (qali[i][j] / maxdis) * 100

data["qali"] = qali

with open(a, "w") as f:
    json.dump(data, f)