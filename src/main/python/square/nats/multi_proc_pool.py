from multiprocessing import Pool
import os
import time


def hello_world(name):
    print("enter:", os.getpid())
    time.sleep(1)
    print("exit:", os.getpid())
    return name.upper()


list_of_movie_names = ["john_wick_1", "john_wick_1", "john_wick_3"]


def demo_multi_processing():
    tic = time.time()
    pool = Pool(processes=os.cpu_count())
    
    res = list(
        pool.apply_async(hello_world, args=(name,)) for name in list_of_movie_names
    )

    pool.close()
    pool.join()

    results = [r.get() for r in res]
    print(results)
    toc = time.time()
    print(f"Completed in {toc - tic} seconds")


if __name__ == "__main__":
    demo_multi_processing()
