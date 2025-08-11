from typing import List


class Solution:
    def _num_ways_helper(self, n: int, k: int, num_ways_memo: List[int]) -> int:
        if n == 1:
            return k
        if n == 2:
            return k * k
        if n in num_ways_memo:
            return num_ways_memo[n]
        
        prev_num_ways = self._num_ways_helper(n - 1, k, num_ways_memo)
        prev_num_ways += self._num_ways_helper(n - 2, k, num_ways_memo)
        num_ways_memo[n] = prev_num_ways * (k - 1)
        return num_ways_memo[n]

    def num_ways(self, n: int, k: int) -> int:
        if n == 0 or k == 0:
            return 0
        return self._num_ways_helper(n, k, {})


if __name__ == '__main__':
    s = Solution()
    assert s.num_ways(0, 2) == 0
    assert s.num_ways(1, 2) == 2
    assert s.num_ways(2, 2) == 4
    assert s.num_ways(3, 3) == 24
    assert s.num_ways(4, 3) == 66