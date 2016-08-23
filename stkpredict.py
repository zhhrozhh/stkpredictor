
# coding: utf-8

# In[31]:

import json
import numpy
import google
import urllib.request
import csv
import io
import matplotlib.pyplot as plt
from time import strptime
import random
import math
get_ipython().magic('matplotlib inline')
def dump_list(v):
    res = []
    for i in v:
        if type(i)!=list:
            res.append(i)
        else:
            res += dump_list(i)
    return res


# In[2]:

class Date:
    def __init__(self,y=0,m=0,d=0,**dic):
        if not len(dic):
            self.y = y
            self.m = m
            self.d = d
        else:
            d = dic['date']
            self.d = int(d[:d.index('-')])
            d = d[d.index('-')+1:]
            self.m = strptime(d[:d.index('-')],'%b').tm_mon 
            self.y = int(d[d.index('-')+1:])
    def isLeapY(self):
        return not(self.y%400)or((not(self.y%4))and(self.y%100))
    def ttnm(self):
        if(self.m==2):
            return(29 if self.isLeapY() else 28)-self.d+1
        if((self.m%2)and(self.m<8))or((not self.m%2)and(self.m>7)):
            return 31-self.d+1
        if((not self.m%2)and(self.m<8))or((self.m%2)and(self.m>7)):
            return 30-self.d+1
    def ttny(self):
        dd = 366 if self.isLeapY() else 365
        dd = dd-self.d
        for i in range(1,self.m):
            dd = dd - Date(self.y,i,1).ttnm()
        return dd+1
    def __add__(self,b):
        if not isinstance(b,(int,float)):
            return -1
        dd = int(b)
        res = Date(self.y,self.m,self.d)
        while dd >= res.ttny():
            dd = dd-res.ttny()
            res.y += 1
            res.m = 1
            res.d = 1
        while dd >= res.ttnm():
            dd = dd-res.ttnm()
            res.m += 1
            res.d = 1
        res.d += dd
        return res
    def __eq__(self,oth):
        return (self.y==oth.y) and (self.m==oth.m) and (self.d==oth.d)
    def __gt__(self,oth):
        if self.y!=oth.y:
            return self.y>oth.y
        if self.m!=oth.m:
            return self.m>oth.m
        if self.d!=oth.d:
            return self.d>oth.d
        return False
    def __lt__(self,oth):
        if self!=oth:
            return not self>oth
        return False
    def __le__(self,oth):
        return self<oth or self==oth
    def __ge__(self,oth):
        return self>oth or self==oth
    def __ne__(self,oth):
        return not self==oth
    def __sub__(self,oth):
        if type(oth)==int:
            res = Date(self.y-int(oth/365)-1,1,1)
            while res+oth!=self:
                res += 1
            return res
        if self<=oth:
            return -1
        b = oth
        res = 0
        while b<self:
            tny = b.ttny()
            b+=tny
            res+=tny
        while b>self:
            b-=1
            res-=1
        return res
    def __str__(self):
        return str(self.y)+"."+str(self.m)+"."+str(self.d)
    def __repr__(self):
        return self.__str__()


# In[59]:

class Funct:
    def __init__(self):
        return
    def f(self,x):
        return 0
    def df(self,x):
        return 0
    def inv(self,x):
        return 0
class Sigmoid(Funct):
    def __init__(self):
        return
    def f(self,x):
        return math.tanh(x)
    def df(self,x):
        return 1/(math.cosh(x)**2)
    def inv(self,x):
        return math.atanh(x)


# In[147]:

class bpnn:
    def __init__(self,n):
        self.val = list(range(0,n))
        self.dval = list(range(0,n))
        af = Sigmoid()
        self.actf = [af for i in range(0,n)]
        self.weight = {}
        self.dweight = {}
        self.layer = []
        self.layerN = 0
        self.n = n
        self.i = [[] for i in range(0,n)]
        self.o = [[] for i in range(0,n)]
        self.eta = 0.38
    def layerize(self,*a):
        if type(a[0])==int:
            self.layer.append(list(a))
            self.layerN += 1
            self.val.append(1)
            self.dval.append(0)
        elif type(a[0])==list:
            for i in a:
                self.layerize(*i)
    def connect(self,l1,l2):
        if type(l1)!=list:
            l1 = [l1]
        if type(l2)!=list:
            l2 = [l2]
        for i in l1:
            for j in l2:
                self.weight[str(i)+','+str(j)] = random.uniform(-0.16,0.16)
                self.dweight[str(i)+','+str(j)] = 0
                self.i[j].append(i)
                self.o[i].append(j)
    def configBias(self):
        self.o += [[] for i in range(0,self.layerN)]
        for i in range(1,self.layerN):
            self.connect(self.n+i,self.layer[i])
    def configLayer(self):
        for i in range(1,self.layerN):
            self.connect(self.layer[i-1],self.layer[i])
    def ff(self,x):
        for i in range(0,len(x)):
            self.val[self.layer[0][i]] = x[i]
        for i in range(1,self.layerN):
            for j in self.layer[i]:
                self.val[j] = 0
                for k in self.i[j]:
                    self.val[j] += self.weight[str(k)+','+str(j)]*self.val[k]
                self.val[j] = self.actf[j].f(self.val[j])
        return [self.val[i] for i in self.layer[self.layerN-1]]
    def bp(self,y):
        for i in range(0,len(y)):
            self.dval[self.layer[self.layerN-1][i]] = self.val[self.layer[self.layerN-1][i]]-y[i]
        for i in range(0,self.layerN-1)[::-1]:
            for j in self.layer[i]:
                dEdg = 0
                dEdw = 0
                for k in self.o[j]:
                    dk = self.actf[k].df(self.actf[k].inv(self.val[k]))
                    dEdg += self.dval[k] *                    self.weight[str(j)+','+str(k)] * dk
                        
                    dEdw = self.dval[k] * dk * self.val[j]
                    self.dweight[str(j)+','+str(k)] = dEdw
                for k in self.o[j]:
                    self.weight[str(j)+','+str(k)] -= self.eta*self.dweight[str(j)+','+str(k)]
                self.dval[j]=dEdg;
    def train(self,x,y,t=1):
        if type(x)!=list:
            x = [x]
        if type(y)!=list:
            y = [y]
        for i in range(0,t):
            self.ff(x)
            self.bp(y)


# In[145]:

scode = 'SNE'
sdate = ['Dec','25','2015']
edate = ['Aug','14','2016']
'startdate=Aug+25%2C+2015&enddate=Aug+23%2C+2016&num=30&ei=f8S7V-jjC9aieLazitAE'
f = urllib.request.urlopen('http://www.google.com/finance/historical?q='+                           scode+                           '&startdate='+sdate[0]+'+'+sdate[1]+'%2C+'+sdate[2]+                           '&enddate='+edate[0]+'+'+edate[1]+'%2C+'+edate[2]+                           '&output=csv')
s = csv.reader(io.StringIO(f.read().decode('utf-8-sig')))
s = list(s)
s = s[1:]
"""r = []
for i in range(0,len(s)):
    s[i][0] = Date(date=s[i][0])
    if i > 0 and s[i][0]-s[i-1][0]>1:
        for j in range(1,s[i][0]-s[i-1][0]):
            c = s[i-1][:]
            c[0] = s[i][0]+j
            r.append(c)
s = s + r
s = sorted(s,key=lambda x:x[0])"""
hi = [float(x[2])/60 for x in s]
lo = [float(x[3])/60 for x in s]
clo = [float(x[4])/60 for x in s]


# In[146]:

nn = bpnn(20)
nn.layerize(*range(0,9))
nn.layerize(*range(9,19))
nn.layerize(19)
nn.configLayer()
nn.configBias()
#train
pat = []
a = len(hi)-2
for j in range(0,1000):
    for i in range(0,len(hi)-3):
        x = clo[i:i+3]+hi[i:i+3]+lo[i:i+3]
        y = (clo[i+3]-clo[i+2])/clo[i+2]
        pat.append(y)
        
        nn.train(x,y,5)
    print(j,' ',end='')    
    #pat.append([x,y])


# In[142]:

pat = []
res = []
Y = []
for i in range(0,len(hi)-3):
    x = clo[i:i+3]+hi[i:i+3]+lo[i:i+3]
    res.append(nn.ff(x)[0]*clo[i+2]+clo[i+2])
    pat.append(nn.ff(x)[0])
    Y.append(clo[i+3])


# In[143]:

f = plt.figure(figsize = (20,10))

plt.subplot(241)
plt.plot(hi)
plt.subplot(242)
plt.plot(lo)
plt.subplot(243)
plt.plot(clo)
plt.subplot(244)
plt.plot(res)
plt.subplot(245)
plt.plot(pat)
plt.subplot(246)
plt.plot(Y)

