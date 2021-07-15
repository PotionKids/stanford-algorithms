def performance(func, max_size, num_cases, *args, **kwargs):
    from time import time

    start_size = 1

    # sizes = [n for n in range(start_size, max_size + 1)]
    sizes = list()
    times = list()

    for size in range(start_size, max_size + 1):
        print(f"size = {size}")
        start = time()
        try:
            func(size, num_cases, *args, **kwargs)
        except RecursionError:
            break
        end = time()
        sizes.append(size)
        times.append((end - start)/num_cases)

    return sizes, times
