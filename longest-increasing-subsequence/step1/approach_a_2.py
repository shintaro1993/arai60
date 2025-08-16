from typing import List


class Solution:
    def _calculate_max_length(self, position, sequence, nums):
        if position >= len(nums):
            return len(sequence)
        
        lenght1 = self._calculate_max_length(position + 1, sequence, nums)
        if sequence and nums[position] <= sequence[-1]:
            return lenght1
        sequence.append(nums[position])
        lenght2 = self._calculate_max_length(position + 1, sequence, nums)
        sequence.pop()
        return max(lenght1, lenght2)

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

