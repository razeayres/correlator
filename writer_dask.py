# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)
# and Josicleda Galvincio (josicleda@gmail.com)

import gc, os, time
import generator
import functions
import variables
from dask.distributed import Client, Lock, wait, fire_and_forget
from threading import Thread
# from multiprocessing import Pool
# from concurrent.futures import ThreadPoolExecutor, as_completed

def starting(ts, o, reader, gen):
    reader.itf.starting_workers()
    with Client(n_workers=reader.itf.prc) as c:
        time.sleep(30)
        lock = Lock('writer')

        _o = c.scatter(o, broadcast=True)
        _reader = c.scatter(reader, broadcast=True)
        _y = c.scatter(variables.y(reader), broadcast=True)

        reader.itf.processing()
        while True:
            try:
                future = c.submit(functions.statistics, _o, _reader, _y, next(gen.data))
                fire_and_forget(future)
                # ts.append(future)
                # t = Thread(target=wait, args=(future,))
                # t.start()
            except StopIteration:
                # for future in ts:
                #     fire_and_forget(future)
                break

def joining(tj, st):
    while True:
        for t in tj:
            # if t.is_alive():
            print('joining', t)
            wait(t)
                # t.join()
                # tj.remove(t)
        if not st.is_alive():
            break

def data(reader):
    o = "__".join(map(str, [os.path.basename(reader.itf.csvfile).replace('.csv', ''),
                            reader.itf.prm,
                            str(reader.itf.trh).replace('.', '_'),
                            reader.itf.prc,
                            reader.itf.typ])) + '.csv'

    n = 1
    on = o
    while os.path.isfile(o):
        o = on.replace('.csv', ' ('+str(n)+').csv')
        n += 1

    with open(o, 'w') as writer:
        writer.write("t,pearson,rmse,a,b,pc,lim,rtv,rmse0,nash,pbias" + "\n")

    gen = generator.start(reader)

    ts = tj = []
    st = Thread(target=starting, args=(ts, o, reader, gen,))
    # jn = Thread(target=joining, args=(tj, st,))
    st.start()
    # jn.start()
    st.join()
    # if not st.is_alive():
    #     jn.join()
    


        # with ThreadPoolExecutor() as executor:
        #     while True:
        #         try:
        #             executor.submit(wait(c.submit(functions.statistics, _o, _reader, _y, next(gen.data))))
        #         except StopIteration:
        #             break

        # ts =[]
        # while True:
        #     try:
        #         t = Thread(target = wait, args=[c.submit(functions.statistics, _o, _reader, _y, next(gen.data))])
        #         ts.append(t)
        #         t.start()
        #     except StopIteration:
        #         break
        # for t in ts:
        #     t.join()

        # with Pool(processes=20) as pool:
        #     while True:
        #         try:
        #             pool.apply_async(wait(c.submit(functions.statistics, _o, _reader, _y, next(gen.data))))
        #         except StopIteration:
        #             break

    # async with Client(asynchronous=True) as c:
    #     _o = await c.scatter(o, broadcast=True)
    #     _reader = await c.scatter(reader, broadcast=True)
    #     _y = await c.scatter(variables.y(reader), broadcast=True)

    #     reader.itf.processing()
    #     while True:
    #         try:
    #             task = c.submit(functions.statistics, _o, _reader, _y, next(gen.data))
    #             await task
    #         except StopIteration:
    #             break

    # Handling garbage to
    # avoid memory overuse
    gc.collect()

    # Closes the process
    reader.itf.ending_workers()