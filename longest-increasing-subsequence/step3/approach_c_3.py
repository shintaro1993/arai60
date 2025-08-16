import bisect
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        # minimum last values for increasing subsequence of each length
        min_last_values = []
        for num in nums:
            insert_position = bisect.bisect_left(min_last_values, num)
            if insert_position < len(min_last_values):
                min_last_values[insert_position] = num
                continue
            min_last_values.append(num)
        return len(min_last_values)


if __name__ == "__main__":
    s = Solution()
    assert s.lengthOfLIS([]) == 0
    assert s.lengthOfLIS([0]) == 1
    assert s.lengthOfLIS([0, 1]) == 2
    assert s.lengthOfLIS([1, 0]) == 1
    assert s.lengthOfLIS([1, 1]) == 1
    assert s.lengthOfLIS([3, 1, 2]) == 2
    assert s.lengthOfLIS([10, 20, 1, 2, 3]) == 3
    assert s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4
