"""Correctness tests for the two sorting implementations."""
import unittest
from sorting_algorithms import quick_sort, merge_sort


class SortingTests(unittest.TestCase):
    def test_general_cases(self):
        datasets = [
            [], [7], [3, 2, 1], [1, 2, 3],
            [7, -1, 0, -8, 3, 7, 7], [5] * 15,
            [x % 17 for x in range(150, -1, -1)],
        ]
        for dataset in datasets:
            for algorithm in (quick_sort, merge_sort):
                with self.subTest(dataset=dataset[:8], algorithm=algorithm.__name__):
                    original = dataset.copy()
                    result = algorithm(original)
                    self.assertIs(result, original)
                    self.assertEqual(result, sorted(dataset))

    def test_merge_sort_is_stable(self):
        class Record:
            def __init__(self, key, order):
                self.key, self.order = key, order
            def __le__(self, other):
                return self.key <= other.key
        records = [Record(2, 'a'), Record(1, 'b'), Record(2, 'c')]
        merge_sort(records)
        self.assertEqual([r.order for r in records], ['b', 'a', 'c'])


if __name__ == '__main__':
    unittest.main()
