from math import log
import time
from stk_dist import *
from stk_data_set import *
class StkBayes:
    def __init__(self,**arg):
        try:
            self.code = arg['code']
        except:
            self.code = None
        try:
            self.category = arg['category']
        except:
            self.category = DEFAULT_CATEGORY
        try:
            self.k = arg['k']#smoothing parameter
        except:
            self.k = 1
        try:
            self.n = arg['parameter']
        except:
            n=1
        try:
            self.misc = arg['misc']
        except:
            self.misc = {}
    def set_training_data(self,td='Default'):
        if td == 'Default'
            self.training_data = StkDataSet(self.code).getData()
        else:
            self.training_data = td
    def n_gram_train(self,t=0):
        """
            train to predict result for t days from today
            t<n
        """
        if t >= self.n:
            raise Exception('')
        que = Queue_n(self.n)
        self.n_gram_label_counter = {label:0 for label in self.category}
        self.n_gram_feature_counter = {}
        self.n_gram_label_feature_counter = {label:{} for label in self.category}
        if 'training_data' not in dir(self):
            raise Exception('training data not set')
        for data_entry in self.training_data:
            label = category_fit(self.category,data_entry.inc)
            if que.sat:
                counter_inc(self.n_gram_label_counter,label)
                counter_inc(self.n_gram_label_feature_counter[label],que.to_feature_string(t))
                counter_inc(self.n_gram_feature_counter,que.to_feature_string(t))
            que.append(label)
    def n_gram_dist(self,evi):
        res = StkDist(self.category)
        evi_ = [category_fit(entry.inc,self.category) for entry in evi]
        for label in self.category:
            p_label = float(self.n_gram_label_counter[label])/float(sum(self.n_gram_label_counter[label_] for label_ in self.category))
            try:
                p_label *= float(self.n_gram_label_feature_counter[label][evi_]+self.k)/float(self.n_gram_label_counter[label]+self.k*2)
            except:
                p_label = 0
            res.dist[label]=p_label
            res.normalize()
        return res
    def n_day_train(self,t=0):
        que = Queue_n(self.n)
        self.n_day_label_counter = {label:0 for label in self.category}
        self.n_day_feature_counter = {}
        self.





