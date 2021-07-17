def performance(func, max_size, num_cases, *args, **kwargs):
    from time import time
    import numpy as np

    start_size = 10

    sizes = list()
    times = list()

    for size in range(start_size, max_size + 1):
        start = time()
        try:
            func(size, num_cases, *args, **kwargs)
        except RecursionError:
            break
        except:
            break
        end = time()
        sizes.append(size)
        times.append((end - start)/num_cases)

    times = list(map(lambda x: x / (times[0]), times))

    sizes = np.array(sizes)
    times = np.array(times)
    return sizes, times
