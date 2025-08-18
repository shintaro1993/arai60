import math
from typing import List


class Solution:
    def _get_sum_value(self, nums, start, end):
        sum_value = 0
        for i in range(start, end + 1):
            sum_value += nums[i]
        return sum_value

    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_sum_value = -math.inf
        for start in range(len(nums)):
            for end in range(start, len(nums)):
                sum_value = self._get_sum_value(nums, start, end)
                max_sum_value = max(max_sum_value, sum_value)
        return max_sum_value


if __name__ == "__main__":
    s = Solution()
    assert s.maxSubArray([]) == 0
    assert s.maxSubArray([1]) == 1
    assert s.maxSubArray([1, 2]) == 3
    assert s.maxSubArray([1, -2, 3]) == 3
    assert s.maxSubArray([2, -1, 2]) == 3
