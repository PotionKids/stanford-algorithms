from random_array import gen_random_array


def test_merge_sort_size_num_cases(size, num_cases):
    for _ in range(num_cases):
        test_merge_sort_size(size)


def test_merge_sort_size(size):
    arr = gen_random_array(size)
    arr = merge_sort(arr)


def test_merge_sort():
    for size in range(50):
        test_merge_sort_size(size)


def test_merge(size_left, size_right):
    left = sorted(gen_random_array(size_left))
    right = sorted(gen_random_array(size_right))
    merged = merge(left, right)
    assert merged == sorted(left + right)


def merge(left, right):
    l, r, i = 0, 0, 0

    merged = list()

    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            merged.append(left[l])
            l += 1
        else:
            merged.append(right[r])
            r += 1

    if l < len(left):
        merged += left[l:]
    elif r < len(right):
        merged += right[r:]

    return merged


def sort_recursive(arr, start, end):
    if end <= start:
        return arr[start:start+1]

    center = (start + end) // 2

    left = sort_recursive(arr, start, center)
    right = sort_recursive(arr, center+1, end)

    return merge(left, right)


def merge_sort(arr):
    return sort_recursive(arr, 0, len(arr) - 1)


if __name__ == '__main__':
    from performance import performance
    from plot import plot
    import math

    sizes, times = performance(test_merge_sort_size_num_cases, 1000, 100)
    plot(sizes, times, loglog=True)
