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


def pivot_sort_stanford(arr, pivot, start, stop):
    l, r = start, start

    for r in range(start, stop + 1):
        if arr[r] < arr[pivot]:
            arr[l], arr[r] = arr[r], arr[l]
            l += 1

    return l - 1


def pivot_strategy(arr, start, stop, strategy):
    if strategy == 1:
        return start
    if strategy == 2:
        return stop
    if strategy == 3:
        first = arr[start]
        middle = arr[(start + stop) // 2]
        last = arr[stop]
        index = (start, (start + stop) // 2, stop)

        zipped = list(zip(index, (first, middle, last)))

        return sorted(zipped, key=lambda tup: tup[-1])[1][0]
    if strategy == 4:
        return randrange(start, stop + 1)


abc = list()
pivots = list()


def quick_sort_and_count_recursive(arr, start, stop, count):
    if stop <= start:
        abc.append(stop - start)
        pivots.append(-1)
        return 0

    abc.append(stop - start)

    strategy = 1
    rand_pivot = pivot_strategy(arr, start, stop, strategy)
    arr[start], arr[rand_pivot] = arr[rand_pivot], arr[start]

    pivot = pivot_sort_stanford(arr, start, start + 1, stop)
    pivots.append(pivot)
    arr[start], arr[pivot] = arr[pivot], arr[start]

    quick_sort_and_count_recursive(arr, start, pivot - 1, count)
    quick_sort_and_count_recursive(arr, pivot + 1, stop, count)

    count[0] += stop - start


def quick_sort_and_count(arr):
    count = [0]
    quick_sort_and_count_recursive(arr, 0, len(arr) - 1, count)
    return count


if __name__ == '__main__':
    arr_file = open('Problem_Set_3_Quick_Sort_Array.txt', 'r')
    arr = [int(line.strip()) for line in arr_file.readlines()]
    comparisons = quick_sort_and_count(arr)
    print(comparisons[0])
    sorted_arr = sorted(arr)
    assert arr == sorted_arr