
# coding: utf-8

# In[2]:

from functools import reduce
def stkdata(stk):
    return DailyData(stk,['Dec','1','2000'],['Dec','1','2017']).getData()
def mu(dt):
    return reduce(lambda x,y:x+y,dt)/float(len(dt))
def sigma(dt):
    m = mu(dt)
    n = float(len(dt))
    return (reduce(lambda x,y:x+y,[(x-m)**2 for x in dt])/n)**0.5
def cov(dt1,dt2):
    m1 = mu(dt1)
    m2 = mu(dt2)
    res = D_i(0)
    for i in range(len(dt1)):
        res = res + (dt1[i]-m1)*(dt2[i]-m2)
    return res/float(len(dt1))
def __similarity(dt1,dt2):
    s1 = sigma(dt1)
    s2 = sigma(dt2)
    return cov(dt1,dt2)//(s1*s2)
def __similarity_cos(dt1,dt2):
    ab = reduce(lambda x,y:x+y,[dt1[i]*dt2[i] for i in range(len(dt1))])
    aa = reduce(lambda x,y:x+y,[x**2 for x in dt1])**0.5
    bb = reduce(lambda x,y:x+y,[x**2 for x in dt2])**0.5
    return ab//(aa*bb)
def stk_covSimilarity(stk1,stk2,nd = 9999):
    dt1 = stkdata(stk1)
    dt2 = stkdata(stk2)
    wsize = len(dt1)
    n = min(len(dt2) - len(dt1),nd)
    res = []
    for i in range(n):
        res.append(__similarity(dt1,dt2[n-i:n-i+wsize]))
    return mu(res)
def stk_cosSimilarity(stk1,stk2,nd = 9999):
    dt1 = stkdata(stk1)
    dt2 = stkdata(stk2)
    wsize = len(dt1)
    n = min(len(dt2)-len(dt1),nd)
    res = []
    for i in range(n):
        res.append(__similarity_cos(dt1,dt2[n-i:n-i+wsize]))
    return mu(res)



def dicIncDef(dic,key):
    try:
        dic[key]+=1
    except:
        dic[key]=1


# In[1]:

class D_i:
    def __init__(self,l,**arg):
        if not l:
            self.inc = 0
            self.o = 0
            self.h = 0
            self.l = 0
            self.c = 0
            self.v = 0
            return
        self.inc = (float(arg['close'])-float(arg['open']))*100.0/l
        if arg['s_avg']:
            self.inc = (float(arg['open'])/2+float(arg['close'])/2)*100/l-100
        self.o = float(arg['open'])
        self.c = float(arg['close'])
        self.h = float(arg['high'])
        self.l = float(arg['low'])
        self.v = float(arg['volume'])/10000.0
    def __add__(self,oth):
        res = D_i(0)
        res.inc = self.inc+oth.inc
        res.h = self.h+oth.h
        res.l = self.l+oth.l
        res.o = self.o+oth.o
        res.c = self.c+oth.c
        res.v = self.v+oth.v
        return res
    def __sub__(self,oth):
        res = D_i(0)
        res.inc = self.inc-oth.inc
        res.h = self.h-oth.h
        res.l = self.l-oth.l
        res.o = self.o-oth.o
        res.c = self.c-oth.c
        res.v = self.v-oth.v
        return res
    def __mul__(self,oth):
        res = D_i(0)
        res.inc = self.inc*oth.inc
        res.h = self.h*oth.h
        res.l = self.l*oth.l
        res.o = self.o*oth.o
        res.c = self.c*oth.c
        res.v = self.v*oth.v
        return res
    def __truediv__(self,oth):
        res = D_i(0)
        res.inc = self.inc/oth
        res.h = self.h/oth
        res.l = self.l/oth
        res.o = self.o/oth
        res.c = self.c/oth
        res.v = self.v/oth
        return res
    def __floordiv__(self,oth):
        res = D_i(0)
        res.inc = self.inc/oth.inc
        res.h = self.h/oth.h
        res.l = self.l/oth.l
        res.o = self.o/oth.o
        res.c = self.c/oth.c
        res.v = self.v/oth.v
        return res
    def __pow__(self,oth):
        res = D_i(0)
        res.inc = self.inc**oth
        res.h = self.h**oth
        res.l = self.l**oth
        res.o = self.o**oth
        res.c = self.c**oth
        res.v = self.v**oth
        return res
    def __str__(self):
        return str([self.inc,self.o,self.h,self.l,self.c,self.v])


# In[3]:

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
def plt_data(data,**arg ):
    att = 'inc'
    if 'att' in arg:
        att = arg['att']
    factor = 1.0
    if 'factor' in arg:
        factor=arg['factor']
    yshift = 0
    if 'yshift' in arg:
        yshift = arg['yshift']
    p = [getattr(d,att)*factor+yshift for d in data]
    return plt.plot(p) 


# In[4]:

import copy
import urllib
import urllib.request
import csv
import io
class DailyData:
    def __init__(self,scode,sdate,edate):
        f = urllib.request.urlopen('http://www.google.com/finance/historical?q='+                            scode+                           '&startdate='+sdate[0]+'+'+sdate[1]+'%2C+'+sdate[2]+                           '&enddate='+edate[0]+'+'+edate[1]+'%2C+'+edate[2]+                           '&output=csv')
        s = csv.reader(io.StringIO(f.read().decode('utf-8-sig')))
        self.s = list(s)[1:][::-1]
    def getData(self,**arg):
        setavg = False
        #print(arg)
        if 's_avg' in arg:
            setavg = True
        res = []
        l = float(self.s[0][1])/2+float(self.s[0][4])/2
        for x in self.s:
            res.append(D_i(l,open = x[1],high=x[2],low=x[3],close=x[4],volume=x[5],s_avg=setavg))
            l = float(x[4])
            if setavg:
                l = (float(x[1])+float(x[4]))/2
        self.data = res
        return copy.deepcopy(res)
    def getdData(self,**arg):
        dvar = ['inc']
        if 'dvar' in arg:
            dvar = arg['dvar']
        order = 1
        if 'order' in arg:
            order = arg['order']
        try:
            dt = copy.deepcopy(self.data)
        except:
            dt = copy.deepcopy(self.getData())
        res = [dt,copy.deepcopy(dt)]
        for od in range(order):
            for dv in dvar:
                for i in range(1,len(dt)):
                    setattr( res[(od+1)%2][i-1],dv, getattr(res[od%2][i],dv)-getattr(res[od%2][i-1],dv))
        return res[order%2]
        


# In[5]:

class RScale:
    def __init__(self,**arg):
        if 'rule' in arg:
            self.rule = arg['rule']
        else:
            self.rule = [-12.5,-10.0,-5.0,-2.5,-0.0001,0.0001,2.5,5.0,10.0,12.5]
        if 'dist' in arg:
            self.dist = arg['dist']
        else:
            self.dist = {x:1 for x in self.rule}
    def fit(self,x):
        for i in range(len(self.rule)-1):
            if x>=self.rule[i] and x<=self.rule[i+1]:
                return self.rule[i] if self.rule[i]>=0 else self.rule[i+1]
            if x>=self.rule[len(self.rule)-1]:
                return self.rule[len(self.rule)-1]
            if x<=self.rule[0]:
                return self.rule[0]
    def disp(self):
        for x in self.rule:
            if x<0:
                print(self.dist[x],end = '___')
                print(x,end = '___')
            else:
                print(x,end = '___')
                print(self.dist[x],end = '___')
    def exp(self,dist):
        mexp = 0
        Mexp = 0
        for i in range(len(self.rule)):
            #print(mexp,Mexp)
            if self.rule[i]>0:
                mexp+=self.rule[i]*dist[self.rule[i]]
                try:
                    Mexp+=self.rule[i+1]*dist[self.rule[i]]
                except:
                    Mexp+=self.rule[i]*dist[self.rule[i]]
            else:
                Mexp+=self.rule[i]*dist[self.rule[i]]
                if i:
                    mexp+=self.rule[i-1]*dist[self.rule[i]]
                else:
                    mexp+=self.rule[i]*dist[self.rule[i]]
        return (mexp,Mexp)
    def counter(self):
        return {x:0 for x in self.rule}
    def features(self):
        return {x:{} for x in self.rule}



# In[6]:

class Queue_n:
    def __init__(self,n,**arg):
        self.n = n
        if 'queue' in arg:
            self.q = arg['queue']
        else:
            self.q = []
        self.sat = False
    def append(self,x):
        self.q.append(x)
        if len(self.q)>self.n:
            self.q.pop(0)
            self.sat = True
    def tstr(self,cata):
        res = ''
        for i in self.q:
            res+=str(cata.index(i))
        return res


# In[17]:

from math import log
class BbayesSS:
    def __init__(self,**arg):
        if 'code' in arg:
            self.code = arg['code']
        else:
            self.code = 'NONE'
        if 'rule' in arg:
            self.rule = rule
        else:
            self.rule = RScale()
        self.ngram_l = {}
        self.ngram_feature = {}
        self.labelCount = {}
        self.labelFeature = {x:{} for x in self.rule.rule}
        self.featureCount = {}
        self.k = 1
        self.td = False
    def set_training_data(self,td):
        self.td = True
        self.tdata = td
    def ngram_train(self,n,sdate=[],edate=[]):
        que = Queue_n(n)
        self.ngram_l[n] = {x:0 for x in self.rule.rule}
        self.ngram_feature[n] = {x:{} for x in self.rule.rule}
        tdata = []
        if not self.td:
            tdata = DailyData(self.code,sdate,edate).getData()
        else:
            tdata = self.tdata
        for x in tdata:
            y = self.rule.fit(x.inc)
            if que.sat:
                dicIncDef(self.ngram_l[n],y)
                dicIncDef(self.ngram_feature[n][y],que.tstr(self.rule.rule))
            que.append(y)
    def ngram_dist(self,n,evi):
        try:
            ff = [self.rule.fit(evi[i].inc) for i in range(n)]
        except:
            ff = evi
        ff = Queue_n(n,queue=ff).tstr(self.rule.rule)
        res = self.rule.counter()
        dist = {}
        for key in self.ngram_l[n]:
            p_key = log(float(self.ngram_l[n][key]+self.k)/float(sum(self.ngram_l[n][qq] for qq in self.ngram_l[n])+self.k))
            try:
                p_key += log(float(self.ngram_feature[n][key][ff]+self.k)/float(self.ngram_l[n][key]+self.k*2))
            except:
                p_key += log(float(self.k)/float(sum(self.ngram_l[n][k] for k in self.ngram_l[n])+self.k*2))
            dist[key] = p_key
        s = sum(2**dist[x] for x in dist)
        for x in dist:
            dist[x]=2**dist[x]/s
            if dist[x]<0.00001:
                dist[x]=0
        return dist
    def n_day_bayes_train(self,n,sdate,edate):
        que = Queue_n(n)
        if not self.td:
            tdata = DailyData(self.code,sdate,edate).getData()
        else:
            tdata = self.tdata
        self.featureCount = {x:{f:self.k for f in self.rule.rule} for x in range(n)}
        self.featureCount_l = {f:self.k for f in self.rule.rule}
        p_vol = 0
        p_h = 0
        p_l = 0
        for x in tdata:
            inc = self.rule.fit(x.inc)
            if que.sat:
                dicIncDef(self.labelCount,inc)
                for i in range(n):
                    self.featureCount[i][que.q[i]]+=1
                    self.featureCount_l[que.q[i]]+=1
                    try:
                        dicIncDef(self.labelFeature[inc][i],que.q[i])
                    except:
                        self.labelFeature[inc][i]={que.q[i]:1}
                try:
                    dicIncDef(self.labelFeature[inc]['v'],p_vol)
                except:
                    self.labelFeature[inc]['v'] = {p_vol:1}
                try:
                    dicIncDef(self.labelFeature[inc]['h'],p_h)
                except:
                    self.labelFeature[inc]['h'] = {p_h:1}
                try:
                    dicIncDef(self.labelFeature[inc]['l'],p_l)
                except:
                    self.labelFeature[inc]['l'] = {p_l:1}
            que.append(inc)
            p_vol = int(x.v/1000)
            p_h = int(x.h)
            p_l = int(x.l)
    def n_day_bayes_dist(self,n,nday,weight = False):
        dist = {}
        w = [1 for x in range(n)]
        if weight:
            w = [float(i+self.k)/float(sum(range(n))+n*self.k) for i in range(n)]
        for inc in self.rule.rule:
            p = log(float(self.labelCount[inc]+self.k)/float(sum(self.labelCount[x] for x in self.labelCount)+self.k))
            for i in range(n):
                try:
                    f = self.rule.fit(nday[i].inc)
                except:
                    f = nday[i]
                try:
                    p+=w[i]*log(float(self.labelFeature[inc][i][f]+self.k)/float(self.labelCount[inc]+2*self.k))
                except Exception as e:
                    p+=w[i]*log(float(self.labelCount[inc]+self.k)/float(sum(self.labelCount[x] for x in self.labelCount)+self.k))
            dist[inc]=p
        s = sum(2**dist[x] for x in dist)
        for x in dist:
            dist[x]=2**dist[x]/s
            if dist[x]<0.00001:
                dist[x]=0
        return dist
    def n_day_bayes_codist(self,n,nday,coset=[]):
        sim = [stk_covSimilarity(self.code,oth.code) for oth in coset]
        codist = [oth.n_day_bayes_dist(n,nday) for oth in coset]
        mdist = self.n_day_bayes_dist(n,nday)
        for i in range(len(sim)):
            for f in self.rule.rule:
                mdist[f]+=sim[i]*codist[i][f]
        s = sum(mdist[x] for x in mdist)
        for x in mdist:
            mdist[x] = mdist[x]/s
        return mdist
        


# In[19]:

yrd = BbayesSS(code = 'yrd')
sdate = ['Dec','1','2000']
edate = ['Dec','29','2016']
data = DailyData('yrd',sdate,edate).getData()
x = BbayesSS(code = 'x')
bac = BbayesSS(code = 'bac')
jpm = BbayesSS(code = 'jpm')
#lmt = BbayesSS(code = 'lmt')
nyt = BbayesSS(code = 'nyt')
coset = [x,bac,jpm,nyt]
yrd.n_day_bayes_train(9,sdate,edate)
for stk in coset:
    print(stk.code)
    stk.n_day_bayes_train(9,sdate,edate)
yrd.n_day_bayes_codist(9,data[-9:])

