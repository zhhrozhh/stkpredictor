from stk_alu import *
class StkAnaBlock:
	def __init__(self,scode,period,k,**arg):
		self.scode = scode
		self.hourly = period == 'hourly'
		self.alus = [StkALU(code = scode,n=i) for i in range(1,k+1)]