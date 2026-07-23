"""Tim Sort

A simplified version of the hybrid stable sort used by Python and Java:
split the list into small runs, sort each run with insertion sort, then
merge the runs together using the same merge step as merge sort.
"""

from typing import List

MIN_RUN = 32


def insertion_sort(arr: List[int], left: int, right: int) -> None:
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr: List[int], left: int, mid: int, right: int) -> None:
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]

    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1


def tim_sort(arr: List[int]) -> List[int]:
    arr = arr[:]
    n = len(arr)

    for start in range(0, n, MIN_RUN):
        end = min(start + MIN_RUN - 1, n - 1)
        insertion_sort(arr, start, end)

    size = MIN_RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge(arr, left, mid, right)
        size *= 2

    return arr


if __name__ == "__main__":
    sample = [23, 10, 20, 11, 12, 6, 7, 41, 5, 33, 9, 1]
    print("Before:", sample)
    print("After: ", tim_sort(sample))
