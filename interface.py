# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)
# and Josicleda Galvincio (josicleda@gmail.com)

class handler(object):
    def __init__(self, csvfile=None, prm=None, trh=None, prc=None):
        self.csvfile = csvfile
        self.prm = prm
        self.trh = trh
        self.prc = prc

    def show(self, t):
        l = [len(i) for i in t]
        d = max(l) * '-'
        for i in [d] + t + [d]:
            print(i)

    def credits(self):
        t1 = 'correlator v1.0  Copyright (C) 2019'
        t2 = 'Rodrigo de Queiroga Miranda / Josicleda Domiciano Galvincio'
        t3 = 'This program comes with ABSOLUTELY NO WARRANTY'
        t4 = 'This is free software, and you are welcome to redistribute it'
        self.show([t1, t2, t3, t4])

    def definitions(self):
        print('Usage: python <input> <n_pars> <threshold> <n_procs>')
        if not self.prm == None:
            print('Number of paramaters selected to model: ' + str(self.prm))
    
    def reading_data(self):
        print('[1] Reading data...')

    def starting_workers(self):
        print('[2] Starting workers...')

    def processing(self):
        print('[3] Processing...')

    def ending_workers(self):
        print('[4] Ending workers...')