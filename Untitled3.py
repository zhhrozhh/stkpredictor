
# coding: utf-8

# In[10]:

def dicIncDef(dic,key):
    try:
        dic[key]+=1
    except:
        dic[key]=1


# In[39]:

class D_i:
    def __init__(self,l,**arg):
        self.inc = (float(arg['open'])/2+float(arg['close'])/2)*100/l-100
        self.o = float(arg['open'])
        self.c = float(arg['close'])
        self.h = float(arg['high'])
        self.l = float(arg['low'])
        self.v = float(arg['volume'])
    def __str__(self):
        return str([self.inc,self.o,self.h,self.l,self.c,self.v])


# In[36]:

class DailyData:
    def __init__(self,scode,sdate,edate):
        f = urllib.request.urlopen('http://www.google.com/finance/historical?q='+                            scode+                           '&startdate='+sdate[0]+'+'+sdate[1]+'%2C+'+sdate[2]+                           '&enddate='+edate[0]+'+'+edate[1]+'%2C+'+edate[2]+                           '&output=csv')
        s = csv.reader(io.StringIO(f.read().decode('utf-8-sig')))
        self.s = list(s)[1:][::-1]
    def getData(self):
        res = []
        l = float(self.s[0][1])/2+float(self.s[0][4])/2
        for x in self.s:
            res.append(D_i(l,open = x[1],high=x[2],low=x[3],close=x[4],volume=x[5]))
            l = (float(x[1])+float(x[4]))/2
        return res


# In[117]:

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



# In[101]:

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


# In[344]:

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
        ff = [self.rule.fit(evi[i].inc) for i in range(n)]
        ff = Queue_n(n,queue=ff).tstr(self.rule.rule)
        res = self.rule.counter()
        dist = {}
        for key in self.ngram_l[n]:
            p_key = log(float(self.ngram_l[n][key]+self.k)/float(sum(self.ngram_l[n][qq] for qq in self.ngram_l[n])+self.k))
            print('p_key',p_key)
            try:
                print('t',float(self.ngram_feature[n][key][ff]+self.k)/float(self.ngram_l[n][key]+self.k*2))
                p_key += log(float(self.ngram_feature[n][key][ff]+self.k)/float(self.ngram_l[n][key]+self.k*2))
            except:
                print('e',log(float(self.k)/float(sum(self.ngram_l[n][k] for k in self.ngram_l[n])+self.k*2)))
                #p_key += log(float(self.k)/float(self.ngram_l[n][key]+self.k*2))
                p_key += log(float(self.k)/float(sum(self.ngram_l[n][k] for k in self.ngram_l[n])+self.k*2))
            dist[key] = p_key
        s = sum(2**dist[x] for x in dist)
        for x in dist:
            dist[x]=2**dist[x]/s
            if dist[x]<0.00001:
                dist[x]=0
        #s = sum(dist[x] for x in dist)
        #for x in dist:
        #    dist[x]/=s
        #    if dist[x]<0.00001:
        #        dist[x]=0
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
                f = self.rule.fit(nday[i].inc)
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


# In[348]:

a=BbayesSS(code = 'yrd')

data = DailyData('yrd',['Dec','18','2015'],['Dec','20','2016']).getData()

a.n_day_bayes_train(5,['Dec','1','2015'],['Dec','20','2016'])
nd_dist = a.n_day_bayes_dist(5,data[-5:])
print('=======')
for x in nd_dist:
    print(x,nd_dist[x])
print(sum(nd_dist[x] for x in nd_dist))
print(a.rule.exp(nd_dist))
print('=======')
a.ngram_train(2,['Dec','1','2015'],['Dec','20','2016'])
ng_dist = a.ngram_dist(2,data[-2:])
for x in ng_dist:
    print(x,ng_dist[x])
print(sum(ng_dist[x] for x in ng_dist))
print(a.rule.exp(ng_dist))

