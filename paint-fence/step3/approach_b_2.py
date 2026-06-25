class Solution:
    def num_ways(self, n: int, k: int) -> int:
        if n < 0:
            raise ValueError("n must be a non-negative integer")
        if k < 0:
            raise ValueError("k must be a non-negative integer")   
        if n == 0 or k == 0:
            return 0     
        if n == 1:
            return k
        if n == 2:
            return k * k

        same_last_two = k
        diff_last_two = k * (k - 1)
        for _ in range(n - 2):
            new_same_last_two = diff_last_two
            new_diff_last_two = (same_last_two + diff_last_two) * (k - 1)
            same_last_two = new_same_last_two
            diff_last_two = new_diff_last_two
        return same_last_two + diff_last_two


if __name__ == '__main__':
    s = Solution()
    assert s.num_ways(0, 2) == 0
    assert s.num_ways(1, 2) == 2
    assert s.num_ways(2, 2) == 4
    assert s.num_ways(3, 3) == 24
    assert s.num_ways(4, 3) == 66