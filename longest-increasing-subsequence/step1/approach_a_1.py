from typing import List


class Solution:
    def _is_LIS(self, sequence):
        for i in range(len(sequence) - 1):
            if sequence[i] >= sequence[i+1]:
                return False
        return True

    def _calculate_max_length(self, position, subsequence, nums):
        if position >= len(nums):
            if self._is_LIS(subsequence):
                return len(subsequence)
            return 0
        
        length1 = self._calculate_max_length(position + 1, subsequence, nums)
        subsequence.append(nums[position])
        length2 = self._calculate_max_length(position + 1, subsequence, nums)
        subsequence.pop()
        return max(length1, length2)

    def lengthOfLIS(self, nums: List[int]) -> int:
        return self._calculate_max_length(0, [], nums)
    

if __name__ == '__main__':
    s = Solution()
    assert s.lengthOfLIS([]) == 0
    assert s.lengthOfLIS([0]) == 1
    assert s.lengthOfLIS([0, 1]) == 2
    assert s.lengthOfLIS([1, 0]) == 1
    assert s.lengthOfLIS([1, 1]) == 1
    assert s.lengthOfLIS([3, 1, 2]) == 2
    assert s.lengthOfLIS([10, 20, 1, 2, 3]) == 3
    assert s.lengthOfLIS([10,9,2,5,3,7,101,18]) == 4

