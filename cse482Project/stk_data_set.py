from stk_data_entry import StkDataEntry
import copy
import urllib
import urllib.request
import csv
import io
class StkDataSet:
    def __init__(self,scode,hourly = False,sdate=['Dec','1','1960'],edate=['Dec','1','2200']):
        if not hourly:
            f = urllib.request.urlopen('http://www.google.com/finance/historical?q='+ \
                           scode+\
                           '&startdate='+sdate[0]+'+'+sdate[1]+'%2C+'+sdate[2]+\
                           '&enddate='+edate[0]+'+'+edate[1]+'%2C+'+edate[2]+\
                           '&output=csv')
            s = csv.reader(io.StringIO(f.read().decode('utf-8-sig')))
            self.raw_dataset = list(s)[1:][::-1]
        if hourly:
            f = urllib.request.urlopen('https://www.google.com/finance/getprices?i=3600&p=600d&f=d,o,h,l,c,v&df=cpct&q='+scode.upper())
            s = csv.reader(io.StringIO(f.read().decode('utf-8-sig')))
            self.raw_dataset = list(s)[7:]
    def getData(self,**arg):
        setavg = 's_avg' in arg and arg['s_avg']
        res = []
        l = float(self.raw_dataset[0][1])/2+float(self.raw_dataset[0][4])/2
        for x in self.raw_dataset:
            try:
                res.append(StkDataEntry(l,open = x[1],high=x[2],low=x[3],close=x[4],volume=x[5],s_avg=setavg))
                l = float(x[4])
                if setavg:
                    l = (float(x[1])+float(x[4]))/2
            except:
                pass
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

from stt_tool import *
def stk_covSimilarity(stk1,stk2,hourly=False,nd = 9999):
    """
        stk1: stock code for stock with less historical data
        stk2: stock code for stock with sufficient historical data
        nd: steps of convolution
        result will be returned as StkDataEntry
    """
    dt1 = stkdata(stk1)
    dt2 = stkdata(stk2)
    wsize = len(dt1)
    n = min(len(dt2) - len(dt1),nd)
    res = []
    for i in range(n):
        res.append(__similarity(dt1,dt2[n-i:n-i+wsize]))
    return mu(res)
def stk_cosSimilarity(stk1,stk2,hourly=False,nd = 9999):
    """
        stk1: stock code for stock with less historical data
        stk2: stock code for stock with sufficient historical data
        nd: steps of convolution
        result will be returned as StkDataEntry
    """
    dt1 = StkDataSet(stk1,hourly).getData()
    dt2 = StkDataSet(stk2,hourly).getData()
    wsize = len(dt1)
    n = min(len(dt2)-len(dt1),nd)
    res = []
    for i in range(n):
        res.append(__similarity_cos(dt1,dt2[n-i:n-i+wsize]))
    return mu(res)


