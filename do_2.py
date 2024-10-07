import sys, json, random

sys.setrecursionlimit(1000000)

with open("ALL_FIN4_final_31genes_4098species.phy","r") as f:
    ali = f.read()

a = random.randint(17800,17900)
b = a+100

print(a,b)
# input()

def needleman_wunsch(seq1, seq2, matrix, gap=-2):
    rows = len(seq1) + 1
    cols = len(seq2) + 1
    score_matrix = [[0] * cols for _ in range(rows)]

    for i in range(1, rows):
        score_matrix[i][0] = score_matrix[i - 1][0] + gap
    for j in range(1, cols):
        score_matrix[0][j] = score_matrix[0][j - 1] + gap

    for i in range(1, rows):
        for j in range(1, cols):
            match_score = score_matrix[i - 1][j - 1] + matrix(seq1[i - 1], seq2[j - 1])
            # (
            #     match if seq1[i - 1] == seq2[j - 1] else mismatch
            # )
            delete_score = score_matrix[i - 1][j] + gap
            insert_score = score_matrix[i][j - 1] + gap
            score_matrix[i][j] = max(match_score, delete_score, insert_score)

    alllen = 0
    # alignment = []
    i, j = rows - 1, cols - 1
    while i > 0 and j > 0:
        score_current = score_matrix[i][j]
        score_diag = score_matrix[i - 1][j - 1]
        score_up = score_matrix[i - 1][j]

        if score_current == score_diag + matrix(seq1[i - 1], seq2[j - 1]):
            if (seq1[i - 1] != seq2[j - 1]):
                alllen += 1
            # alignment.append((seq1[i - 1], seq2[j - 1]))
            i -= 1
            j -= 1
        elif score_current == score_up + gap:
            alllen += 1
            # alignment.append((seq1[i - 1], "-"))
            i -= 1
        else:
            alllen += 1
            # alignment.append(("-", seq2[j - 1]))
            j -= 1

    while i > 0:
        alllen += 1
        # alignment.append((seq1[i - 1], "-"))
        i -= 1
    while j > 0:
        alllen += 1
        # alignment.append(("-", seq2[j - 1]))
        j -= 1

    # alignment.reverse()

    # ans = len(alignment)

    # for i in alignment:
    #     if i[0] == i[1]:
    #         ans -= 1

    return alllen

ali = ali.splitlines()[1:]
nali = []
qali = {}
for i in ali:
    ec = i.split()
    ec[0] = ec[0].replace("__","_")
    ec[1] = ec[1][a:b].replace("-","")
    if ec[1] == "":
        ec[1] = "A"
    qali[ec[0]] = {}
    nali.append(ec)



print("done.1")

km = lambda x, y: 5 if x == y else -4

print(len(nali))

for ii in range(1950,min(2050,len(nali))):
    i = nali[ii]
    for jj in range(1950,min(2050,len(nali))):
        j = nali[jj]
        print("handle: %s [and] %s" % (i[0],j[0]))
        if i[0] != j[0]:
            qali[i[0]][j[0]] = needleman_wunsch(i[1], j[1], km)


qcc = {}
for i in qali:
    if qali[i] != {}:
        qcc[i] = qali[i]

print("done.2")

q = {
    "startpoint": a,
    "endpoint": b,
    "qali": qcc
}

with open("output_14.json","w") as f:
    json.dump(q, f)