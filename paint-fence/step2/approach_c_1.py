class Solution:
    def num_ways(self, n: int, k: int) -> int:
        if n == 0 or k == 0:
            return 0
        if n == 1:
            return k
        if n == 2:
            return k * k
        
        num_ways_memo = [0] * n
        num_ways_memo[0] = k
        num_ways_memo[1] = k * k
        for i in range(2, n):
            num_ways_memo[i] = (num_ways_memo[i-1] + num_ways_memo[i-2]) * (k - 1)
        return num_ways_memo[n-1]
    

if __name__ == '__main__':
    s = Solution()
    assert s.num_ways(0, 2) == 0
    assert s.num_ways(1, 2) == 2
    assert s.num_ways(2, 2) == 4
    assert s.num_ways(3, 3) == 24
    assert s.num_ways(4, 3) == 66