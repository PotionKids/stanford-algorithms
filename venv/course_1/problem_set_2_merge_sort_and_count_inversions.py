def merge_and_count(left, right):
    l, r, i = 0, 0, 0

    merged = list()
    count = 0
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            merged.append(left[l])
            l += 1
        else:
            merged.append(right[r])
            count += len(left) - l
            r += 1

    if l < len(left):
        merged += left[l:]
    elif r < len(right):
        merged += right[r:]

    return merged, count


def sort_and_count_recursive(arr, start, end):
    if end <= start:
        return arr[start:start+1], 0

    center = (start + end) // 2

    left, count_left = sort_and_count_recursive(arr, start, center)
    right, count_right = sort_and_count_recursive(arr, center+1, end)

    merged, count_merged = merge_and_count(left, right)
    return merged, count_left + count_right + count_merged


def sort_and_count_inversions(arr):
    return sort_and_count_recursive(arr, 0, len(arr) - 1)


if __name__ == '__main__':
    arr_file = open('problem_set_2_merge_sort_and_count_inversions.txt', 'r')
    arr = [int(line.strip()) for line in arr_file.readlines()]
    sorted_arr, inversions = sort_and_count_inversions(arr)
    print(inversions)