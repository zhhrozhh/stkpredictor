from functools import reduce
def mu(dt):
    """
        average of data set dt
    """
    return reduce(lambda x,y:x+y,dt)/float(len(dt))
def sigma(dt):
    """
        variance of data set dt
    """
    m = mu(dt)
    n = float(len(dt))
    return (reduce(lambda x,y:x+y,[(x-m)**2 for x in dt])/n)**0.5
def cov(dt1,dt2):
    """
        covariance of data set dt1 and dt2
    """
    if len(dt1)-len(dt2):
        raise Exception("dimension error")
    m1 = mu(dt1)
    m2 = mu(dt2)
    res = D_i(0)
    for i in range(len(dt1)):
        res = res + (dt1[i]-m1)*(dt2[i]-m2)
    return res/float(len(dt1))
def __similarity_cov(dt1,dt2):
    """
        raw definition of cov similarity 
    """
    s1 = sigma(dt1)
    s2 = sigma(dt2)
    return cov(dt1,dt2)//(s1*s2)
def __similarity_cos(dt1,dt2):
    """
        raw definition of cos similarity
    """
    ab = reduce(lambda x,y:x+y,[dt1[i]*dt2[i] for i in range(len(dt1))])
    aa = reduce(lambda x,y:x+y,[x**2 for x in dt1])**0.5
    bb = reduce(lambda x,y:x+y,[x**2 for x in dt2])**0.5
    return ab//(aa*bb)

def counter_inc(dic,key):
    try:
        dic[key]+=1
    except:
        dic[key]=1