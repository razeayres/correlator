# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)
# and Josicleda Galvincio (josicleda@gmail.com)

from itertools import product

class start(object):
	def __init__(self, reader):
		self.reader = reader
		self.trs = ['(','(1/','numpy.log(','numpy.log10(','numpy.sqrt(','**2)','numpy.exp(']
		self.ops = ['+','-','/','*']
		self.x_str = 'self.x'
		self.data_str = 'self.reader.data'
		self.data = self.generate()

	def mount(self, op, wl, tr):
		t = ()
		for a in xrange(len(wl)):
			wlr = 'numpy.array(' + self.data_str + '[' + "'" + wl[a] + "'" + '])'
			if tr[a] == '**2)':
				if a != len(wl)-1:
					t = t + ('(',wlr,tr[a],op[a])
				else:
					t = t + ('(',wlr,tr[a])
			else:
				if a != len(wl)-1:
					t = t + (tr[a],wlr,')',op[a])
				else:
					t = t + (tr[a],wlr,')')
		x = self.x_str + " = " + "".join(t)
		t = ','.join(t).replace("'","").replace('"','').replace(',','').replace('[','').replace(']','').replace('))',')').replace('((','(').replace('numpy.','').replace('array(','').replace(self.data_str,'').replace('**2)','**2')
		return((t,x))

	def generate(self):
		ops = product(self.ops, repeat=self.reader.itf.prm-1)
		for i in ops:
			wls = product(self.reader.wls, repeat=self.reader.itf.prm)
			for j in wls:
				trs = product(self.trs, repeat=self.reader.itf.prm)
				for l in trs:
					yield(self.mount(i, j, l))
				del trs
			del wls
		del ops