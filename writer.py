# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)
# and Josicleda Galvincio (josicleda@gmail.com)

import multiprocessing, gc, os
import generator
import functions
import variables

class data(object):
    def __init__(self, reader):
        self.reader = reader
        self.write()

    def opt_y(self):
        from functools import partial

        # Pre-process the y values to use
        # in pearson calculations
        y = variables.y(self.reader)
        y = partial(functions.statistics, self.reader, y)
        return(y)

    def write(self):
        o = "__".join(map(str, [os.path.basename(self.reader.itf.csvfile).replace('.csv', ''),
                               self.reader.itf.prm,
                               str(self.reader.itf.trh).replace('.', '_'),
                               self.reader.itf.prc,
                               self.reader.itf.typ])) + '.csv'

        n = 1
        on = o
        while os.path.isfile(o):
            o = on.replace('.csv', ' ('+str(n)+').csv')
            n += 1

        with open(o, 'w') as writer:
            self.reader.itf.starting_workers()
            pool = multiprocessing.Pool(processes=self.reader.itf.prc)
            gen = generator.start(self.reader)

            # writer.write("t,pearson,rmse,a,b,pc,lim,rtv,rmse0,nash,pbias,pearson_EQ_B,pearson_EQ_G,pearson_EQ_M,pearson_MCD_8d,pearson_MCD_4d,rmse_EQ_B,rmse_EQ_G,rmse_EQ_M,rmse_MCD_8d,rmse_MCD_4d" + "\n")
            writer.write("t,pearson,rmse,a,b,pc,lim,rtv,rmse0,nash,pbias" + "\n")

            y = self.opt_y()
            self.reader.itf.processing()
            for i in pool.imap(y, gen.data, 1000):
                if not i.qc == 1:
                    # r = [i.t,
                    #      i.pearson,
                    #      i.rmse,
                    #      i.cov.a,
                    #      i.cov.b,
                    #      i.pc,
                    #      i.lim,
                    #      i.rtv,
                    #      i.rmse0,
                    #      i.nash,
                    #      i.pbias,
                    #      i.pearson_EQ_B,
                    #      i.pearson_EQ_G,
                    #      i.pearson_EQ_M,
                    #      i.pearson_MCD_8d,
                    #      i.pearson_MCD_4d,
                    #      i.rmse_EQ_B,
                    #      i.rmse_EQ_G,
                    #      i.rmse_EQ_M,
                    #      i.rmse_MCD_8d,
                    #      i.rmse_MCD_4d]
                    r = [i.t,
                         i.pearson,
                         i.rmse,
                         i.cov.a,
                         i.cov.b,
                         i.pc,
                         i.lim,
                         i.rtv,
                         i.rmse0,
                         i.nash,
                         i.pbias]
                    r = map(str, r)
                    writer.write(",".join(r) + "\n")

            # Handling garbage to
            # avoid memory overuse
            gc.collect()

            # Closes the process
            self.reader.itf.ending_workers()
            pool.close()
            pool.join()