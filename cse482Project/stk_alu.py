from math import log
import time
from stk_dist import *
from stk_data_set import *
from stt_tool import *
DEFAULT = 'DEFAULT'
class StkALU:
    def __init__(self,**arg):
        try:
            self.code = arg['code']
        except:
            self.code = None
        try:
            self.category = sorted(arg['category'])
        except:
            self.category = DEFAULT_CATEGORY
        try:
            self.k = arg['k']#smoothing parameter
        except:
            self.k = 1
        try:
            self.n = arg['n']
        except:
            n=1
        try:
            self.misc = arg['misc']
        except:
            self.misc = {}
        try:
            self.hourly = arg['hourly']
        except:
            self.hourly = False
    def set_training_data(self,td=DEFAULT):
        if td == DEFAULT:
            self.training_data = StkDataSet(self.code,self.hourly).getData()
        else:
            self.training_data = td
    def training_data_size(self):
        if 'training_data' not in dir(self):
            raise Exception('training data not set')
        return len(self.training_data)
    def n_gram_train(self,t=0):
        """
            train to predict result for t days from today
            t<n
            n gram:
            P(Ld | L{d-1},L{d-2},...,L{d-n}) propto Count(Ld,L{d-1},...,L{d-n})/Count(Ld,L{d-1},...,L{d-n})
            if Count(Ld,L{d-1},...,L{d-n}) == 0,
            use a feature that similar to Ld,...,L{d-n}
        """
        if t >= self.n:
            raise Exception('t error')
        if 'training_data' not in dir(self):
            raise Exception('training data not set')        
        que = Queue_n(self.n)
        self.n_gram_t = t
        self.n_gram_feature_counter = {}
        self.n_gram_label_feature_counter = {label:{} for label in self.category}

        for data_entry in self.training_data:
            label = category_fit(self.category,data_entry.inc)
            if que.sat:
                counter_inc(self.n_gram_label_feature_counter[label],que.to_feature_string(t))
                counter_inc(self.n_gram_feature_counter,que.to_feature_string(t))
                #self.n_gram_feature_set.add(que.to_feature_string(t))
            que.append(label)
        #print(self.n_gram_label_feature_counter)
    def n_gram_dist(self,evi = DEFAULT):
        if evi == DEFAULT:
            evi = self.training_data[-self.n+self.n_gram_t:]
        feature = str([category_fit(self.category,e.inc) for e in evi[-self.n_gram_t:]])
        res = StkDist(category = self.category)
        for label in self.category:
            try:
                res.dist[label] = float(self.n_gram_label_feature_counter[label][feature]+self.k)\
                /float(self.n_gram_feature_counter[feature]+self.k*2)
            except:
                sim = {}
                for feature_ in self.n_gram_label_feature_counter[label]:
                    sim[feature_] = feature_similarity(feature,feature_)
                feature_ = max(sim,key = lambda x:sim[x])
                try:
                    res.dist[label] = float(self.n_gram_label_feature_counter[label][feature_]+self.k)\
                    /float(self.n_gram_feature_counter[feature_]+self.k*2)
                except:
                    res.dist[label] = 0
        res.normalize()
        return res
    def n_day_naive_bayes_train(self,t=0):
        """
            assume that P(L1,...,Ln|C) = P(L1|C)...P(Ln|C)
        """
        if t>=self.n:
            raise Exception('t error')
        if 'training_data' not in dir(self):
            raise Exception('training data not set')
        self.n_day_naive_bayes_t = t
        self.n_day_naive_bayes_label_counter = {label:0 for label in self.category}
        self.n_day_naive_bayes_feature_counter = {}
        self.n_day_naive_bayes_label_feature_counter = {label:{} for label in self.category} 
        que = Queue_n(self.n)
        for data_entry in self.training_data:
            label = category_fit(self.category,data_entry.inc)
            if que.sat:
                for i in range(self.n-t):
                    feature_ = str((i,que.q[i]))
                    counter_inc(self.n_day_naive_bayes_feature_counter,feature_)
                    counter_inc(self.n_day_naive_bayes_label_feature_counter[label],feature_)
                counter_inc(self.n_day_naive_bayes_label_counter,label)
            que.append(label)

    def n_day_naive_bayes_dist(self,**arg):
        if 'evi' in arg:
                evi = arg['evi']
        else:
            evi = self.training_data[-self.n:]
        if 'weight' in arg:
            if arg['weight'] == NORMAL_DEC:
                pass
            elif arg['weight'] == LOG_DEC:
                pass
            elif arg['weight'] == HALF_DEC:
                pass
            else:
                weight = arg['weight']
        else:
            weight = [1 for i in range(self.n-self.n_day_naive_bayes_t)]
        evi_ = [category_fit(self.category,e.inc) for e in evi[-self.n+self.n_day_naive_bayes_t:]]
        evi_ = [str((i,evi_[i])) for i in range(self.n_day_naive_bayes_t)]

        res = StkDist(category = self.category)
        for label in self.category:
            p = log(float(self.n_day_naive_bayes_label_counter[label]+self.k)/float(self.training_data_size()+2*self.k))
            for i in range(self.n_day_naive_bayes_t):
                try:
                    p += log(float(self.n_day_naive_bayes_label_feature_counter[label][evi_[i]]+self.k)\
                        /float(self.n_day_naive_bayes_label_counter[label]+self.k*2))
                except:
                    p += log(float(self.n_day_naive_bayes_label_counter[label]+self.k)\
                        /float(self.training_data_size()+self.k*3))
            res.dist[label] = 2**p
        res.normalize()
        return res;

import stt_tool
def feature_similarity(f1,f2):
    v1 = list(map(float,f1[1:-1].split(',')))
    v2 = list(map(float,f2[1:-1].split(',')))
    return stt_tool.__similarity_cos(v1,v2)


