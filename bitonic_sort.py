"""Bitonic Sort

A parallel-friendly comparison sort that builds bitonic sequences (values
that rise then fall) and repeatedly merges them into fully sorted order.
Classically defined for lists whose length is a power of two; shorter
inputs are padded with +infinity sentinels and unpadded after sorting.
"""

import math
from typing import List

INF = math.inf


def compare_and_swap(arr: List[float], i: int, j: int, ascending: bool) -> None:
    if (arr[i] > arr[j]) == ascending:
        arr[i], arr[j] = arr[j], arr[i]


def bitonic_merge(arr: List[float], low: int, count: int, ascending: bool) -> None:
    if count <= 1:
        return
    mid = count // 2
    for i in range(low, low + mid):
        compare_and_swap(arr, i, i + mid, ascending)
    bitonic_merge(arr, low, mid, ascending)
    bitonic_merge(arr, low + mid, count - mid, ascending)


def bitonic_sort_recursive(arr: List[float], low: int, count: int, ascending: bool) -> None:
    if count <= 1:
        return
    mid = count // 2
    bitonic_sort_recursive(arr, low, mid, True)
    bitonic_sort_recursive(arr, low + mid, count - mid, False)
    bitonic_merge(arr, low, count, ascending)


def bitonic_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    padded_size = 1 << (n - 1).bit_length() if n > 0 else 0
    padded = arr[:] + [INF] * (padded_size - n)

    bitonic_sort_recursive(padded, 0, padded_size, True)

    return padded[:n]


if __name__ == "__main__":
    sample = [23, 10, 20, 11, 12, 6, 7]
    print("                    ")
    print("Before:", sample)
    print("After: ", bitonic_sort(sample))
    print("                    ")
