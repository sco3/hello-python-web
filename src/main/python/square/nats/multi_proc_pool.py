from multiprocessing import Pool
import os
import time

res = []


def hello_world(name):
    print("enter:", os.getpid())
    time.sleep(1)
    print("exit:", os.getpid())
    return name.upper()


def collect(name):
    res.append(name)


def demo_multi_processing():
    tic = time.time()
    pool = Pool(processes=os.cpu_count())

    for i in range(10):
        pool.apply_async(hello_world, args=(f"x{i}",), callback=collect)

    pool.close()
    pool.join()

    print(res)
    toc = time.time()
    print(f"Completed in {toc - tic} seconds")


if __name__ == "__main__":
    demo_multi_processing()
