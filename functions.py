# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)
# and Josicleda Galvincio (josicleda@gmail.com)

import numpy
import variables
from math import sqrt
from copy import copy

class statistics(object):
	def __init__(self, reader, y, chunk):
		# This was received from
		# from the partial function object
		self.y = y
		self.reader = reader

		# This is the real variable argument
		# received from the generator
		self.t, self.x = chunk

		#### Here are the statistics ####
		self.simulate()
		if self.qc == 0:	# qc means Quality Control (0 is okay, while 1 is something wrong)
			self.pearson = self.calc_pearson(self.cov.cov, self.x, self.y)
			self.pearson = self.threshold(self.pearson)
			self.rmse = self.calc_rmse(self.x, self.y)

			self.adjust_zeros(self.y0, self.y)
			if self.qc == 0:	# qc means Quality Control (0 is okay, while 1 is something wrong)
				self.pc = self.calc_pc(self.y0, self.y)
				self.rmse0 = self.calc_rmse(self.y0, self.y)
				self.nash = self.calc_nash(self.y0, self.y)
				self.pbias = self.calc_pbias(self.y0, self.y)
				# self.compare_to_others()

	def simulate(self):
		numpy.seterr('raise')
		try:
			exec(self.x)
			if self.reader.itf.typ in ['log', 'pow']:
				self.x = numpy.ma.log(self.x)	# ajuste nao-linear
				self.x = self.x.filled(0)
			self.x = variables.x(self.x)
			self.cov = variables.cov(self.x, self.y)

			self.y0 = self.cov.a + self.cov.b*self.x.s
			# self.y0[self.y0<0] = 0		# replaces all negatives values by zero
			self.y0 = variables.x(self.y0)
			self.cov0 = variables.cov(self.y0, self.y)

			self.qc = 0
		except:
			self.qc = 1

	# limits are processed
	# in this part of the code
	def adjust_zeros(self, x, y):
		# this was modified to
		# disable the limit def
		self.lim = 0
		self.rtv = 0
		return(None)
		# try:
		# 	r = []
		# 	fsc = 10**6
		# 	vmn = int(min(x.s)*fsc)
		# 	stp = abs(int((max(x.s)/100)*fsc))
		# 	vmx = int(max(x.s)*fsc) - stp
		# 	for i in xrange(vmn, vmx, stp):
		# 		i = float(i)/fsc
		# 		x0 = copy(x.s)
		# 		x0[x0<i] = 0		# replaces all negatives values by zero
		# 		z = zip(x0, y.s)
		# 		c = 0
		# 		for j in z:
		# 			if (j[0] == 0 and j[1] == 0) or (j[0] > 0 and j[1] > 0):
		# 				c += 1
		# 		error = float(c)/len(x0)
		# 		r.append((i, error))

		# 	b = max(r, key=lambda z: z[1])
		# 	self.lim = round(b[0], 2)
		# 	self.rtv = round((1-b[1])*100, 2)
		# 	self.y0.s[self.y0.s<self.lim] = 0
		# except:
		# 	self.qc = 1

	def threshold(self, func):
		r = func
		if self.qc == 0:
			if abs(r) < float(self.reader.itf.trh):
				self.qc = 1
		return(r)

	def calc_pearson(self, cov, x, y):
		r2 = (cov/(y.v * x.v))**2
		r2 = round(r2, 2)
		return(r2)

	def calc_rmse(self, x, y):
		rmse = numpy.sqrt(((y.s-x.s)**2).mean())
		rmse = round(rmse, 2)
		return(rmse)

	def calc_pc(self, x, y):
		pc = (2 * (y.d*x.d).mean())/((y.d**2).mean() + (x.d**2).mean() + (y.s.mean() - x.s.mean())**2)
		pc = round(pc, 2)
		return(pc)

	def calc_nash(self, x, y):
		n = ((x.s - y.s)**2).sum()
		d = ((x.s - x.s.mean())**2).sum()
		nash = 1 - (n/d)
		nash = round(nash, 2)
		return(nash)

	def calc_pbias(self, x, y):
		pbias = 100*((x.s - y.s).sum()/y.s.sum())
		return pbias

	def compare_to_others(self):
		EQ_B = variables.x(numpy.array(self.reader.data['EQ_B']))
		EQ_G = variables.x(numpy.array(self.reader.data['EQ_G']))
		EQ_M = variables.x(numpy.array(self.reader.data['EQ_M']))
		MCD_8d = variables.x(numpy.array(self.reader.data['MCD_8d']))
		MCD_4d = variables.x(numpy.array(self.reader.data['MCD_4d']))
		cov_EQ_B = variables.cov(self.y0, EQ_B)
		cov_EQ_G = variables.cov(self.y0, EQ_G)
		cov_EQ_M = variables.cov(self.y0, EQ_M)
		cov_MCD_8d = variables.cov(self.y0, MCD_8d)
		cov_MCD_4d = variables.cov(self.y0, MCD_4d)

		self.pearson_EQ_B = sqrt(self.calc_pearson(cov_EQ_B.cov, self.y0, EQ_B))
		self.pearson_EQ_G = sqrt(self.calc_pearson(cov_EQ_G.cov, self.y0, EQ_G))
		self.pearson_EQ_M = sqrt(self.calc_pearson(cov_EQ_M.cov, self.y0, EQ_M))
		self.pearson_MCD_8d = sqrt(self.calc_pearson(cov_MCD_8d.cov, self.y0, MCD_8d))
		self.pearson_MCD_4d = sqrt(self.calc_pearson(cov_MCD_4d.cov, self.y0, MCD_4d))
		self.rmse_EQ_B = self.calc_rmse(self.y0, EQ_B)
		self.rmse_EQ_G = self.calc_rmse(self.y0, EQ_G)
		self.rmse_EQ_M = self.calc_rmse(self.y0, EQ_M)
		self.rmse_MCD_8d = self.calc_rmse(self.y0, MCD_8d)
		self.rmse_MCD_4d = self.calc_rmse(self.y0, MCD_4d)