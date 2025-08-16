from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_lengths_by_ending_position = [1] * len(nums)
        for current_index in range(1, len(nums)):
            for previous_index in range(current_index):
                if nums[previous_index] >= nums[current_index]:
                    continue
                max_lengths_by_ending_position[current_index] = max(
                    max_lengths_by_ending_position[current_index],
                    max_lengths_by_ending_position[previous_index] + 1,
                )
        return max(max_lengths_by_ending_position)


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
