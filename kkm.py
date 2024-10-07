# 引入库
import numpy as np
import random as rd
from scipy.optimize import minimize
import pickle

N = 5
M = 3
L = 3
K = 1


class model:
    def __init__(self):

        self.c1 = np.ones((N, M))  # 本组数据
        self.c2 = np.ones((L, K))  # 外组数据
        self.maxt = 2  # 最多遍历次数
        self.mine = 1000  # 最小误差
        self.step = 10  # 步长
        self.mint = 1  # 最少遍历次数
        self.istraining = 0

    def save(self, files):
        f = open(files, "wb")
        s = [self.c1, self.c2]
        pickle.dump(s, f)
        f.close()

    def read(self, files):
        f = open(files, "rb")
        s = pickle.load(f)
        self.c1 = s[0]
        self.c2 = s[1]
        f.close()

    def b(self, a=np.array([])):  # 标准化
        #    print(a)
        mx = a.max()
        for i in range(0, len(a)):
            a[i] /= mx
        return a

    #  print(a,1)
    def sumResidual(self):  # 求当前残差和
        r = 1
        for c in self.residual:
            for dc in c:
                r += np.exp(-dc[0])
        return r

    def addId(self, Id, i):
        if Id < N * M:
            self.c1[Id % N][(Id // N) % M] += i
        else:
            self.c2[(Id - N * M) % L][(Id - N * M) % K] += i

    def change(self):  # 处理变动函数
        i = 0
        for c in range(0, len(self.residual)):
            maxyResidual = -1
            maxId = 0
            id1 = -1
            for dc in range(0, len(self.residual[c])):
                yResidual = 0
                for y in self.residual[c][dc]:
                    #        print (y,dc)
                    yResidual = yResidual + np.exp(y)
                if maxyResidual <= yResidual:
                    maxyResidual = yResidual
                    maxId = id1
                id1 = id1 + 1
            self.addId(i, self.getStep() * maxId)
            i = i + 1

    def getDistance(self, vector1=np.array([]), vector2=np.array([])):
        #  print((vector1-vector2),427)
        return np.sum((vector1 - vector2) ** 2)

    def compute(self, tree=np.array([[[]]]), l=np.array([[]]), goal=np.array([[]])):
        for i in range(0, len(tree)):
            r = np.array([])
            for j in range(0, 48):
                maxId = self.fmax(self.allf, goal[i], args=(tree[i], l[i]))
                r = np.append(r, maxId)
                for d in range(0, 3):
                    self.addId(j, d - 1)
                    #              print(maxId.x,5244)
                    self.residual[j][d][i] = self.allf(
                        goal[i], tree[i], l[i]
                    ) / self.allf(maxId.x, tree[i], l[i])
                    self.addId(j, 1 - d)

        #   print(r)

    def fmax(self, func, x0, args=(), **kwargs):
        return minimize(
            lambda x, tree, l: -func(x, tree, l),
            x0,
            args=args,
            options={"maxiter": 100},
            **kwargs
        )

    def jac(self, x=np.array([]), tree=np.array([[]]), l=np.array([])):
        d = np.zeros((48))
        #    print(tree,l,12341234)
        treeDistance = np.array([])
        for j in range(0, len(tree)):
            treeDistance = np.append(treeDistance, self.getDistance(tree[j], x))
        for i in range(0, len(treeDistance)):
            d = d + self.df(treeDistance, l, i)

    def allf(self, x=np.array([]), tree=np.array([[]]), l=np.array([])):
        rt = 0
        #   print(tree,l,12432)
        treeDistance = np.array([])
        for j in range(0, len(tree)):
            treeDistance = np.append(treeDistance, self.getDistance(tree[j], x))
        #   print(treeDistance[j])
        #  print(treeDistance,234)
        #  if not self.istraining:
        #   print(treeDistance)
        for i in range(0, len(treeDistance)):
            rt += self.f(treeDistance, l, i)
        return rt

    def df(self, r=np.array([[]]), l=np.array([]), i=0):
        j = 0
        rt = np.zeros((48))
        while j < len(r):
            if r[j] == 0:
                r[j] += 0.0001
            if j == i:
                for i1 in range(0, N):
                    for i2 in range(0, M):
                        rt[i1 * 9 + i2 * 3] += (
                            (i1 - 2)
                            * (r[j] ** (i1 - 3))
                            * (l[j] ** (i2 - 1))
                            * self.c1[i1][i2]
                        )
            #                     # print(rt[i1*9+i2*3+i3],i1,i2,i3,r[j],l[j](r[j]**(i1-3)),(l[j]**(i2-1)),(v[j]**(i3-1)),7426)
            else:
                for i1 in range(0, N):
                    for i2 in range(0, M):
                        rt[i1 * 1 + i2 * 1 + n * M] += (
                            (i1 - 1)
                            * (r[j] ** (i1 - 2))
                            * (l[j] ** (i2 - 0))
                            * self.c2[i1][i2]
                        )
            j = j + 1
        # print(rt,2937)
        return rt

    def f(self, r=np.array([]), l=np.array([]), i=0):
        j = 0
        score = 0
        #     if not self.istraining:
        #         print(l)
        #     print(r,l)
        while j < len(r):
            if r[j] == 0:
                r[j] += 0.0001
            if j == i:
                for i1 in range(0, N):
                    for i2 in range(0, M):
                        #     if not self.istraining:
                        #          print(r[j],i1,l[j],i2,self.c1[i1][i2],816)
                        score = (
                            score
                            + (r[j] ** (i1 - 2)) * (l[j] ** (i2 - 1)) * self.c1[i1][i2]
                        )
            else:
                for i1 in range(0, L):
                    for i2 in range(0, K):
                        #        print(r[j],i1,l[j],i2)
                        score = (
                            score
                            + (r[j] ** (i1 - 1)) * (l[j] ** (i2 - 0)) * self.c2[i1][i2]
                        )
            j = j + 1
        return score

    def getStep(self):
        return np.exp(-rd.random() - self.t) * self.step

    def training(self, tree=np.array([[[]]]), l=np.array([[]]), goal=np.array([[]])):
        # 第一层是样本个数，第二层是对应基因树
        self.istraining = 1
        self.residual = np.zeros(
            (48, 3, len(tree))
        )  # 共4层，最外面一层是不同变量，第二层是移动量，第三层是不同样本
        self.t = 0
        tree = tree.astype(np.float16)
        for i in tree:
            for j in tree:
                self.b(j)
        l = l.astype(np.float16)
        for i in l:
            self.b(i)
        goal = goal.astype(np.float16)
        for i in goal:
            self.b(i)

        print("begin")
        while (
            (self.t < self.maxt) and (self.mine < self.sumResidual())
        ) or self.t < self.mint:
            self.compute(tree, l, goal)
            print(self.t)
            self.change()
            self.t += 1
        self.istraining = 0

    def worked(self, tree=np.array([[]]), l=np.array([])):

        tree = tree.astype(np.float16)
        mx = tree.max()
        for i in tree:
            self.b(i)
        l = l.astype(np.float16)
        self.b(l)
        return self.fmax(self.allf, np.mean(tree, axis=0), args=(tree, l)).x * mx


a=model()
a.read('model1.model')
print(a.worked(np.array([[500,600,300],[500,300,200]]),np.array([5,1])))
