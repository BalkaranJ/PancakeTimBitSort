# Sorting Algorithms

This document explains the three sorting algorithms implemented in this
repository: [pancake_sort.py](pancake_sort.py), [tim_sort.py](tim_sort.py), and
[bitonic_sort.py](bitonic_sort.py).

---

## Pancake Sort — [pancake_sort.py](pancake_sort.py)

**Idea:** Imagine a stack of pancakes of different sizes. The only move you
have is a spatula that can flip over the top `k` pancakes at once. Pancake
sort repeatedly finds the largest unsorted pancake and uses two flips to
move it to its correct position at the bottom of the unsorted portion.

### `flip(arr, k)`
Reverses the sublist `arr[0..k]` in place (`arr[:k+1]`). This is the only
"move" the algorithm is allowed — everything else is built from flips.

### `pancake_sort(arr)`
For each `size` from `len(arr)` down to `2`:
1. Find the index of the largest value within the first `size` elements
   (`arr[:size]`).
2. If that max is already at the end of the unsorted region (`size - 1`),
   do nothing — it's already in place.
3. Otherwise:
   - Flip the list up to `max_index` to bring the max value to the front
     (`flip(arr, max_index)`).
   - Flip the list up to `size - 1` to send the max value from the front
     down to its correct resting position at the end of the unsorted
     region (`flip(arr, size - 1)`).
4. Shrink the unsorted region by one and repeat.

Each pass guarantees one more element (the current largest) is placed
correctly, similar to selection sort, but "moving" an element is done via
two reversals instead of a direct swap.

**Complexity:** O(n²) comparisons, O(n) flips.

---

## Tim Sort — [tim_sort.py](tim_sort.py)

**Idea:** A simplified version of the hybrid algorithm used internally by
Python and Java. It exploits the fact that insertion sort is fast on small
or nearly-sorted lists, and merge sort is fast at combining already-sorted
lists. The list is chopped into small chunks ("runs"), each run is
insertion-sorted, and then runs are merged together pairwise, doubling the
merged size each pass.

### `MIN_RUN = 32`
The size of each initial chunk. Real-world Timsort picks this dynamically;
here it's fixed for simplicity.

### `insertion_sort(arr, left, right)`
Sorts the sublist `arr[left..right]` in place using classic insertion
sort: each element is compared backward against already-sorted elements
and shifted until it lands in the correct spot.

### `merge(arr, left, mid, right)`
Merges two adjacent, already-sorted sublists — `arr[left..mid]` and
`arr[mid+1..right]` — into a single sorted run covering `arr[left..right]`.
It copies both halves out (`left_part`, `right_part`), then repeatedly
takes the smaller front element from either half and writes it back into
`arr`, followed by copying over any leftovers.

### `tim_sort(arr)`
1. **Run creation:** Walk the list in blocks of `MIN_RUN` and
   insertion-sort each block.
2. **Merging:** Starting with `size = MIN_RUN`, repeatedly merge adjacent
   blocks of the current `size` using `merge`, then double `size` and
   repeat until `size >= n`. This is the same doubling merge pattern as
   bottom-up merge sort, just seeded with pre-sorted runs instead of
   single elements.

**Complexity:** O(n log n) worst case, with better real-world performance
on partially sorted data because the initial runs are already ordered.

---

## Bitonic Sort — [bitonic_sort.py](bitonic_sort.py)

**Idea:** A comparison network originally designed for parallel hardware.
It works by recursively building **bitonic sequences** — sequences that
strictly increase then strictly decrease (or vice versa) — and then
merging each bitonic sequence into a fully sorted one. Classic bitonic
sort requires the input length to be a power of two, so this
implementation pads shorter lists with `+infinity` sentinels and strips
them off at the end.

### `compare_and_swap(arr, i, j, ascending)`
Compares `arr[i]` and `arr[j]` and swaps them if they're out of order
relative to the desired direction (`ascending=True` means `arr[i]` should
end up `<= arr[j]`). This is the basic building block of the network.

### `bitonic_merge(arr, low, count, ascending)`
Takes a bitonic sequence of length `count` starting at `low` and turns it
into a fully sorted sequence (in the given direction). It compares each
element in the first half against its partner in the second half
(`compare_and_swap`), which splits the sequence into two smaller bitonic
sequences where every element in one half is less than every element in
the other. It then recursively merges each half.

### `bitonic_sort_recursive(arr, low, count, ascending)`
Builds a bitonic sequence out of an arbitrary sequence, then merges it:
1. Recursively sort the first half in ascending order.
2. Recursively sort the second half in descending order.
   (Together, an ascending run followed by a descending run *is* a
   bitonic sequence.)
3. Call `bitonic_merge` on the whole range to merge that bitonic sequence
   into one sorted run in the requested direction.

### `bitonic_sort(arr)`
Pads `arr` with `INF` sentinels up to the next power of two
(`1 << (n - 1).bit_length()`), runs `bitonic_sort_recursive` on the padded
list in ascending order, then slices off the first `n` elements — the
sentinels always sort to the end, so the real values end up correctly
sorted in front.

**Complexity:** O(n log² n) comparisons, but comparisons at each stage are
independent of each other, which is what makes this algorithm well suited
to parallel/hardware execution rather than raw single-threaded speed.
