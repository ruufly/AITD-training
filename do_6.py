import numpy as np

def sdf(a=np.array([[]])):
    s=np.array([])
    for i in a:
        for j in a:
            s=np.append(j)


print(sdf(np.array([[1,2,3],[4,5,6],[7,8,9]])))