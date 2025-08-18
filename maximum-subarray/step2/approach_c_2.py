import math
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_sum = -math.inf
        prefix_sum = 0
        min_prefix_sum = 0
        for num in nums:
            prefix_sum += num
            max_sum = max(max_sum, prefix_sum - min_prefix_sum)
            min_prefix_sum = min(min_prefix_sum, prefix_sum)
        return max_sum


if __name__ == "__main__":
    s = Solution()
    assert s.maxSubArray([]) == 0
    assert s.maxSubArray([1]) == 1
    assert s.maxSubArray([1, 2]) == 3
    assert s.maxSubArray([1, -2, 3]) == 3
    assert s.maxSubArray([2, -1, 2]) == 3 
    assert s.maxSubArray([-1]) == -1
