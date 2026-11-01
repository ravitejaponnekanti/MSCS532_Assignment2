"""MSCS-532 Assignment 2: divide-and-conquer sorting implementations.

Both functions sort in ascending order and modify the list supplied by caller.
The simple last-element pivot in quick_sort is deliberate: it exposes
worst-case behavior on sorted and reverse-sorted datasets.
"""

from typing import List, TypeVar

T = TypeVar('T')


def quick_sort(items: List[T]) -> List[T]:
    """In-place Lomuto Quick Sort with an explicit stack.

    Time: O(n log n) average, O(n^2) worst case.
    Extra space: O(log n) typical / O(n) worst for pending ranges.
    This implementation is NOT stable.
    """
    if len(items) <= 1:
        return items

    pending = [(0, len(items) - 1)]
    while pending:
        low, high = pending.pop()
        if low >= high:
            continue

        pivot = items[high]
        boundary = low - 1
        # Elements <= pivot move into the left partition.
        for index in range(low, high):
            if items[index] <= pivot:
                boundary += 1
                items[boundary], items[index] = items[index], items[boundary]
        pivot_index = boundary + 1
        items[pivot_index], items[high] = items[high], items[pivot_index]

        if low < pivot_index - 1:
            pending.append((low, pivot_index - 1))
        if pivot_index + 1 < high:
            pending.append((pivot_index + 1, high))

    return items


def merge_sort(items: List[T]) -> List[T]:
    """Stable top-down Merge Sort using one reusable auxiliary array.

    Time: Theta(n log n) best/average/worst for this unoptimized merge.
    Extra space: Theta(n) for the auxiliary buffer plus O(log n) stack.
    """
    if len(items) <= 1:
        return items

    aux = [None] * len(items)

    def sort_range(start: int, end: int) -> None:
        if end - start <= 1:
            return
        mid = (start + end) // 2
        sort_range(start, mid)
        sort_range(mid, end)

        left, right = start, mid
        for dest in range(start, end):
            # <= resolves ties by choosing the left occurrence: stability.
            if left < mid and (right >= end or items[left] <= items[right]):
                aux[dest] = items[left]
                left += 1
            else:
                aux[dest] = items[right]
                right += 1
        items[start:end] = aux[start:end]

    sort_range(0, len(items))
    return items


if __name__ == '__main__':
    example = [12, 4, 9, 2, 18, 9, 7]
    print('Original:', example)
    print('Quick Sort:', quick_sort(example.copy()))
    print('Merge Sort:', merge_sort(example.copy()))
