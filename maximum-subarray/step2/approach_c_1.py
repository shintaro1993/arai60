import math
from typing import List


class Solution:
    def _get_sum_value(self, prefix_sums, start, end):
        return prefix_sums[end] - prefix_sums[start]

    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        prefix_sums = []
        prefix_sum = 0
        for num in nums:
            prefix_sums.append(prefix_sum)
            prefix_sum += num
        prefix_sums.append(prefix_sum)

        max_sum_value = -math.inf
        for start in range(len(nums)):
            for end in range(start, len(nums) + 1):
                sum_value = self._get_sum_value(prefix_sums, start, end)
                max_sum_value = max(max_sum_value, sum_value)
        return max_sum_value


if __name__ == "__main__":
    s = Solution()
    assert s.maxSubArray([]) == 0
    assert s.maxSubArray([1]) == 1
    assert s.maxSubArray([1, 2]) == 3
    assert s.maxSubArray([1, -2, 3]) == 3
    assert s.maxSubArray([2, -1, 2]) == 3
