class StkDataEntry:
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
    def __and__(self,oth):
        res = D_i(0)
        res.inc = self.inc*oth
        res.h = self.h*oth
        res.l = self.l*oth
        res.o = self.o*oth
        res.c = self.c*oth
        res.v = self.v*oth
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