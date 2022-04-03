# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)
# and Josicleda Galvincio (josicleda@gmail.com)

from sys import argv
from time import time
import multiprocessing, asyncio
import reader
import interface
import writer, writer_dask




if __name__ == '__main__':
    multiprocessing.freeze_support()
    st = time() # starts the timer

    if len(argv) == 6:
        itf = interface.handler(str(argv[1]),       # input file in csv
                                int(argv[2]),       # number of parameters
                                float(argv[3]),     # threshold limit
                                int(argv[4]),       # number of processes
                                str(argv[5]))       # type of fitting (lin, log, pow, exp)
        itf.credits()       # prints the credits
        itf.definitions()   # prints the definitions

        reader = reader.data(itf)
        writer = writer.data(reader)
        # writer = writer_dask.data(reader)
        # asyncio.get_event_loop().run_until_complete(writer_dask.data(reader))
    else:
        itf = interface.handler()
        itf.credits()       # prints the credits
        itf.definitions()   # prints the definitions

    et = time() - st	# stops the timer