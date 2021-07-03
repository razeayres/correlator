# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)
# and Josicleda Galvincio (josicleda@gmail.com)

from math import sqrt
import numpy

class y(object):
    def __init__(self, reader):
        try:
            self.s = numpy.array(reader.data['y'])
            if reader.itf.typ in ['exp', 'pow']:
                self.s = numpy.log(self.s)	# ajuste nao-linear
            self.d = self.s - self.s.mean()
            self.v = sqrt((self.d**2).sum())
        except:
            raise NameError('Column y not found')

class x(object):
    def __init__(self, x):
        self.s = x
        self.d = self.s - self.s.mean()
        self.v = sqrt((self.d**2).sum())

class cov(object):
    def __init__(self, x, y):
        self.cov = (y.d*x.d).sum()
        self.b = ((x.s*y.s).sum()-(x.s.sum()*y.s.sum())/len(x.s))/(((x.s - x.s.mean())**2).sum())
        self.a = y.s.mean()-self.b*x.s.mean()

        self.b = round(self.b, 1)
        self.a = round(self.a, 1)