import matplotlib.pyplot as plt
try:
    get_ipython().magic('matplotlib inline')
except:
    pass
DEFAULT_CATEGORY = [-12.5,-10.0,-7.5,-5.0,-2.5,-1.25,-0.0001,0.0001,1.25,2.5,5.0,7.5,10.0,12.5]
class StkDist:
    def __init__(self,**arg):
        if 'category' in arg:
            self.category = sorted(arg['category'])
        else:
            self.category = DEFAULT_CATEGORY
        self.dist = {x:0 for x in self.category}
    def plot(self,):
        plt.close()
        plt.figure(figsize=(10,4))
        plt.xticks(range(len(self.category)),self.category)
        plt.bar(range(len(self.category)),[self.dist[x] for x in self.category],1,align = 'center')
        plt.show()
    def exp(self):
        for i in range(len(self.category)):
            if self.category[i]>0:
                mexp+=self.category[i]*self.dist[self.category[i]]
                try:
                    Mexp+=self.category[i+1]*self.dist[self.category[i]]
                except:
                    Mexp+=self.category[i]*self.dist[self.category[i]]
            else:
                Mexp+=self.category[i]*self.dist[self.category[i]]
                if i:
                    mexp+=self.category[i-1]*self.dist[self.category[i]]
                else:
                    mexp+=self.category[i]*self.dist[self.category[i]]
        return (mexp,Mexp)
    def normalize(self):
        total = sum([self.dist[label] for label in self.dist])
        for label in self.dist:
            self.dist[label] = self.dist[label]/total
    def __add__(self,oth):
        if self.category != oth.category:
            raise Exception('category error')
        res = StkDist(category = self.category)
        for label in self.category:
            res.dist[label] = self.dist[label]+oth.dist[label]
        return res
    def __sub__(self,oth):
        if self.category != oth.category:
            raise Exception('category error')
        res = StkDist(category = self.category)
        for label in self.category:
            res.dist[label] = self.dist[label]-oth.dist[label]
        return res
    def __mul__(self,oth):
        try:
            scale = float(oth)
        except:
            raise('type error')
        res = StkDist(self.category)
        for label in self.category:
            res.dist[label] = self.dist[label]*scale
        return res
class Queue_n:
    def __init__(self,n,**arg):
        self.n = n
        if 'queue' in arg:
            self.q = arg['queue']
            if len(self.q)>n:
                raise Exception('length error')
        else:
            self.q = []
        self.sat = False
    def append(self,x):
        self.q.append(x)
        if len(self.q)>self.n:
            self.q.pop(0)
            self.sat = True
    def to_feature_string(self,t):
        if self.sat:
            return str(self.q[:self.n-t])
        raise Exception('no enough elements')
def category_fit(category,value):
    for i in range(len(category)-1):
        if value>=category[i] and value<=category[i+1]:
            return category[i] if category[i]>=0 else category[i+1]
        if value>=category[len(category)-1]:
            return category[len(category)-1]
        if value<=category[0]:
            return category[0]
    raise Exception('unknown error')