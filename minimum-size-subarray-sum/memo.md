# 209. Minimum Size Subarray Sum

## step1

方針として、nums[i] が右端に来て、和が target 以上になる subarray を調べていく。最小の長さを更新できそうなら更新する感じで行けそうかな。
二重ループで実装できそう。
(1 <= nums.length <= 105 の制約があるので LeetCode 上では TLE になります。)

```python

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        min_length = len(nums) + 1
        for end in range(len(nums)):
            sum_value = 0
            for start in range(end, -1, -1):
                sum_value += nums[start]
                if sum_value >= target:
                    min_length = min(min_length, end - start + 1)
                    break
        if min_length == len(nums) + 1:
            return 0
        return min_length

```

内側のループで [0, end] の範囲を調べなくても、前回の start の情報を使えそうなのでこの情報を引き継ぐようにする。次の人が start より左側を調べなくてもいいように start を更新しておく。調べ方も end から start 側に範囲を広げていくのではなく、start を end に近づけていくように範囲を狭くして行くのがよさそう。

```python

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        min_length = len(nums) + 1
        sum_value = 0
        start = 0
        for end, num in enumerate(nums):
            sum_value += num
            while sum_value >= target:
                min_length = min(min_length, end - start + 1)
                sum_value -= nums[start]
                start += 1

        if min_length == len(nums) + 1:
            return 0
        return min_length

```

## step2

- https://github.com/SuperHotDogCat/coding-interview/pull/31/files
    - step2 の配列を使わずに書く方法について、外側の while を for で書かない理由がわからなかった。
    - 演算子の前後ではスペースがあった方が個人的に読みやすい。

- https://github.com/olsen-blue/Arai60/pull/50/files
    - bisect_left を使った方法もあるのですね。また後で整理しておこう。

- https://github.com/fhiyo/leetcode/pull/49/files
    - コメントにあるように len(nums) + 1 が解なしの場合であるというのはわかりにくいかもしれない。関数の最初で和をとってはじいておくのもいいかも。
    - left を -1 にする発想はなかった。やっぱり区間を考えるときはいろんな書き方を想定しておく必要がありそう。


リストで累積和を持っておくとループの中がすっきりしてわかりやすいかもしれない。ループの外が少しごちゃっとするけど。

```python

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        if sum(nums) < target:
            return 0
        
        min_length = len(nums)
        prefix_sum = [0]
        for i in range(len(nums)):
            prefix_sum.append(prefix_sum[-1] + nums[i])
        left = 0
        for right in range(1, len(nums) + 1):
            while prefix_sum[right] - prefix_sum[left] >= target:
                min_length = min(min_length, right - left)
                left += 1
        return min_length

```

step1 を整理したもの。変数名は sum_value より total の方が分かりやすいと思う。意図もなく変数名を長くしないように気をつけよう。

```python

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        if sum(nums) < target:
            return 0
        
        min_length = len(nums)
        total = 0
        start = 0
        for end in range(len(nums)):
            total += nums[end]
            while total >= target:
                min_length = min(min_length, end - start + 1)
                total -= nums[start]
                start += 1
        return min_length

```

## step3

この形で練習しました。

```python

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        if sum(nums) < target:
            return 0
        
        min_length = len(nums)
        total = 0
        start = 0
        for end in range(len(nums)):
            total += nums[end]
            while total >= target:
                min_length = min(min_length, end - start + 1)
                total -= nums[start]
                start += 1
        return min_length

```