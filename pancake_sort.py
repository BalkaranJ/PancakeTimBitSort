"""Pancake Sort

Repeatedly flips (reverses) prefixes of the list to move the largest
unsorted element to its final position, like sorting a stack of pancakes
using only a spatula that can flip the top k pancakes.
"""

from typing import List


def flip(arr: List[int], k: int) -> None:
    arr[:k + 1] = arr[:k + 1][::-1]


def pancake_sort(arr: List[int]) -> List[int]:
    arr = arr[:]
    for size in range(len(arr), 1, -1):
        max_index = arr.index(max(arr[:size]))
        if max_index == size - 1:
            continue
        if max_index != 0:
            flip(arr, max_index)
        flip(arr, size - 1)
    return arr


if __name__ == "__main__":
    sample = [23, 10, 20, 11, 12, 6, 7]
    print("                    ")
    print("Before:", sample)
    print("After: ", pancake_sort(sample))
    print("                    ")
