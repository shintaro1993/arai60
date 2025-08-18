import math
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_sum_value = -math.inf
        for start in range(len(nums)):
            sum_value = 0
            for i in range(start, len(nums)):
                sum_value += nums[i]
                max_sum_value = max(max_sum_value, sum_value)
        return max_sum_value


if __name__ == "__main__":
    s = Solution()
    assert s.maxSubArray([]) == 0
    assert s.maxSubArray([1]) == 1
    assert s.maxSubArray([1, 2]) == 3
    assert s.maxSubArray([1, -2, 3]) == 3
    assert s.maxSubArray([2, -1, 2]) == 3
