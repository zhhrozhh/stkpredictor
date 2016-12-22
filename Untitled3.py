
# coding: utf-8

# In[10]:

def dicIncDef(dic,key):
    try:
        dic[key]+=1
    except:
        dic[key]=1


# In[517]:

class D_i:
    def __init__(self,l,**arg):
        #print(arg['close'],arg['open'],l)
        self.inc = (float(arg['close'])-float(arg['open']))*100.0/l
        #print(arg)
        if arg['s_avg']:
            self.inc = (float(arg['open'])/2+float(arg['close'])/2)*100/l-100
        self.o = float(arg['open'])
        self.c = float(arg['close'])
        self.h = float(arg['high'])
        self.l = float(arg['low'])
        self.v = float(arg['volume'])
    def __str__(self):
        return str([self.inc,self.o,self.h,self.l,self.c,self.v])


# In[505]:

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
    #print(exec(r'p = [d.'+arg+' for d in data]'))
    #print(p)
    return plt.plot(p)
    


# In[518]:

mdata = DailyData('yrd',['Dec','18','2015'],['Dec','21','2016'])


# In[521]:

mdata.getData(s_avg = True)
plt_data(mdata.data)
plt_data(mdata.getdData(order=2),factor = 1,yshift = -40)


# In[524]:

import copy
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
                    #res[(od+1)%2][i-1].eval(dv) = res[od%2][i].eval(dv)-res[od%2][i-1].eval(dv)
        return res[order%2]
        


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


# In[357]:

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
            #print('p_key',p_key)
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


# In[544]:

a=BbayesSS(code = 'yrd')

data = DailyData('yrd',['Dec','18','2015'],['Dec','21','2016']).getData()
ddd = 0
a.n_day_bayes_train(9,['Dec','1','2015'],['Dec','21','2016'])
nd_dist = a.n_day_bayes_dist(9,data[-9-ddd:])
a.ngram_train(2,['Dec','1','2015'],['Dec','21','2016'])
ng_dist = a.ngram_dist(2,data[-2-ddd:])
print('Dec','22-',ddd,'2016')
print('=======bayes')
for x in a.rule.rule:
    print(x,nd_dist[x])
#print(sum(nd_dist[x] for x in nd_dist))
print(a.rule.exp(nd_dist))
print('=======ngram')

for x in a.rule.rule:
    print(x,ng_dist[x])
#print(sum(ng_dist[x] for x in ng_dist))
print(a.rule.exp(ng_dist))


# In[ ]:

Dec 22- 0 2016
=======bayes
-12.5 0.0007269219039675484
-10.0 0.11698531056171098
-5.0 0.016498456635787636
-2.5 0.14488204050537568
-0.0001 0.056799016865410314
0.0001 0.021774293313894227
2.5 0.1677546664813892
5.0 0.29046562126816056
10.0 0.1714269556087545
12.5 0.01268671685554932
(1.241775249886257, 4.475643490416318)
=======ngram
-12.5 0.01792486162543823
-10.0 0.01792486162543823
-5.0 0.04915196910680665
-2.5 0.06206248444383042
-0.0001 0.07387242201601357
0.0001 0.06103445502670946
2.5 0.34031361188186415
5.0 0.34368209386886256
10.0 0.01792486162543823
12.5 0.016108378779598507
(1.515169244530631, 4.912157810269509)


Dec 22- 1 2016
=======bayes
-12.5 0.539216811377036
-10.0 0.010141317978182785
-5.0 0.07289947690273746
-2.5 0.04764955392904791
-0.0001 0.02064256353300795
0.0001 0.12621499059425406
2.5 0.016786306639376653
5.0 0.13072426899026532
10.0 0.03453135812064179
12.5 0.00119335193545018
(-6.829995350996995, -5.171976080301118)
=======ngram
-12.5 0.025454329373006714
-10.0 0.025454329373006714
-5.0 0.06979860916755719
-2.5 0.08813227983296873
-0.0001 0.10490306708470283
0.0001 0.08667241922509655
2.5 0.06320757409821053
5.0 0.4880482427003819
10.0 0.025454329373006714
12.5 0.022874819772062138
(1.1014839639928617, 4.875259063251407)


Dec 22- 2 2016
=======bayes
-12.5 0.00015850212926257922
-10.0 0.06557537416769679
-5.0 0.17290161024564757
-2.5 0.3842240197660159
-0.0001 0.049658475115235086
0.0001 0.09180785725414756
2.5 0.08436171672439184
5.0 0.1486693103685445
10.0 0.0026411131406187433
12.5 0
(-3.61528468694102, -0.311772840083032)
=======ngram
-12.5 0.01798730670465596
-10.0 0.01798730670465596
-5.0 0.34267300981246385
-2.5 0.062278692347608265
-0.0001 0.07412977235662925
0.0001 0.061247081570712736
2.5 0.04466564428790071
5.0 0.3448793837573881
10.0 0.01798730670465596
12.5 0.01616449575332921
(-2.1551342401926283, 1.9783536999016462)


Dec 22- 3 2016
=======bayes
-12.5 0.0004942132033657295
-10.0 0.7681562921822028
-5.0 0.062264090647766175
-2.5 0.009309160024048435
-0.0001 0.026227090848645173
0.0001 0.013390010462181698
2.5 0.059330636354406815
5.0 0.014599397104033995
10.0 0.045336041922186356
12.5 0.0008930672511629012
(-9.65703707577049, -6.968350519237443)
=======ngram
-12.5 0.009138667257404743
-10.0 0.1623567651294653
-5.0 0.23059706942699887
-2.5 0.17522011404196214
-0.0001 0.17585053869472853
0.0001 0.17515125695907596
2.5 0.02269291716024768
5.0 0.031641437817021806
10.0 0.009138667257404743
12.5 0.008212566255690203
(-5.356389768170898, -2.2442066840231485)


Dec 22- 4 2016
=======bayes
-12.5 0.0007887375712144071
-10.0 0.0035572054408664895
-5.0 0.4518005845957549
-2.5 0.14777401712715507
-0.0001 0.11668774482631035
0.0001 0.09335977640619544
2.5 0.12276968989171598
5.0 0.06301231126808778
10.0 0.00023163984697848969
12.5 1.829302572108103e-05
(-4.978379402971444, -1.1933857445562992)
=======ngram
-12.5 0.0055696130729848145
-10.0 0.0055696130729848145
-5.0 0.17155243124581088
-2.5 0.10678890152470079
-0.0001 0.280157368279116
0.0001 0.14138800891997688
2.5 0.105742246788785
5.0 0.17265700850649537
10.0 0.0055696130729848145
12.5 0.005005195516160622
(-1.8431866946168356, 1.490857728753346)

