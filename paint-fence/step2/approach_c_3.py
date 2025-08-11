from functools import cache


class Solution:
    @cache
    def num_ways(self, n: int, k: int) -> int:
        if n == 0 or k == 0:
            return 0
        if n == 1:
            return k
        if n == 2:
            return k * k
        return (self.num_ways(n - 1, k) + self.num_ways(n - 2, k)) * (k - 1)
    

if __name__ == '__main__':
    s = Solution()
    assert s.num_ways(0, 2) == 0
    assert s.num_ways(1, 2) == 2
    assert s.num_ways(2, 2) == 4
    assert s.num_ways(3, 3) == 24
    assert s.num_ways(4, 3) == 66
    assert s.num_ways(30, 20) == 1004151076547626230786266566362256795580