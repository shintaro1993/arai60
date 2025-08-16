from typing import List
import bisect


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        min_last_values = []
        for num in nums:
            if not min_last_values or min_last_values[-1] < num:
                min_last_values.append(num)
                continue
            index_to_insert = bisect.bisect_left(min_last_values, num)
            min_last_values[index_to_insert] = num
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
