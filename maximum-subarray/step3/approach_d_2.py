import math
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        max_sum_value = -math.inf
        sum_value_from_min = 0
        for num in nums:
            sum_value_from_min = max(sum_value_from_min + num, num)
            max_sum_value = max(max_sum_value, sum_value_from_min)
        return max_sum_value