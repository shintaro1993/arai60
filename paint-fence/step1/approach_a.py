from typing import List


class Solution:
    def _is_valid_way(self, way: List[int]) -> bool:
        for i in range(len(way) - 2):
            if way[i] == way[i+1] and way[i+1] == way[i+2]:
                return False
        return True

    def _get_num_ways(self, n: int, k: int, way: List[int]) -> int:
        if len(way) == n:
            if self._is_valid_way(way):
                return 1
            return 0
        
        num_ways = 0
        for color in range(k):
            way.append(color)
            num_ways += self._get_num_ways(n, k, way)
            way.pop()
        return num_ways

    def num_ways(self, n: int, k: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return k
        if n == 2:
            return k * k
        return self._get_num_ways(n, k, [])


if __name__ == '__main__':
    s = Solution()
    assert s.num_ways(0, 2) == 0
    assert s.num_ways(1, 2) == 2
    assert s.num_ways(2, 2) == 4
    assert s.num_ways(3, 3) == 24
    assert s.num_ways(4, 3) == 66

    