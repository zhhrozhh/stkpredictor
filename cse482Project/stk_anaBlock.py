from stk_alu import *
class StkAnaBlock:
	def __init__(self,scode,period,k,**arg):
		self.scode = scode
		self.hourly = period == 'hourly'
		self.n_day_alus = [StkALU(code = scode,n=i,hourly = self.hourly) for i in range(1,k+1)]
		self.n_gram_alus = [StkALU(code = scode,n=i,hourly = self.hourly) for i in range(1,k+1)]