from random import randrange


def test_pivot_sort_arr(arr, start, pivot, stop):
    for index in range(start, pivot):
        if arr[index] > arr[pivot]:
            return False

    for index in range(pivot + 1, stop + 1):
        if arr[index] < arr[pivot]:
            return False

    return True


def test_quick_sort_max_size_num_cases(max_size, num_cases):
    for size in range(max_size, max_size + 1):
        test_quick_sort_size_num_cases(size, num_cases)


def test_quick_sort_size_num_cases(size, num_cases):
    from random_array import gen_random_array

    for _ in range(num_cases):
        arr = gen_random_array(size, unique=True, abs_max=10000)
        quick_sort(arr)


def test_uniqueness(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return False
        seen.add(num)
    return True


def pivot_sort(arr, pivot, start, stop):
    l, r = start, stop

    while l < r:
        while l < r and arr[l] < arr[pivot]:
            l += 1
        while l < r and arr[r] > arr[pivot]:
            r -= 1
        arr[l], arr[r] = arr[r], arr[l]

    if l == stop:
        value = stop if arr[l] < arr[pivot] else stop - 1
        return value
    if r == start:
        return pivot
    if l == r:
        return l - 1


def quick_sort_recursive(arr, start, stop):
    if stop <= start:
        return

    rand_pivot = randrange(start, stop + 1)
    arr[start], arr[rand_pivot] = arr[rand_pivot], arr[start]

    pivot = pivot_sort(arr, start, start + 1, stop)
    arr[start], arr[pivot] = arr[pivot], arr[start]

    quick_sort_recursive(arr, start, pivot - 1)
    quick_sort_recursive(arr, pivot + 1, stop)


def quick_sort(arr):
    quick_sort_recursive(arr, 0, len(arr) - 1)


if __name__ == '__main__':
    from performance import performance
    from plot import plot
    import math

    sizes, times = performance(test_quick_sort_size_num_cases, 1000, 50)
    plot(sizes, times, loglog=True)