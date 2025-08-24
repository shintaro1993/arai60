# 213. House Robber II

## step1

House Robber と同じように、直前の家で盗んだ場合と盗まなかった場合のそれぞれの最大額を次の人に渡していけばいいと思う。ただし、入力のリスト上の最後の家のお金を盗めない場合に注意する。例えば、nums = [100, 1, 1, 1000] を考えたとき、4番目の家で1000を盗むことで金額が最大になるが、直前の家で盗んだ場合と盗まなかった場合のどちらの場合も一番目の家で100を盗んだ場合を採用しているため4番目の家で1000を盗めない状況になる。これを回避する為に、「先頭から最後の一つ手前までの家の区間の最大額」と、「二番目の家から最後までの区間の最大額」を計算して、大きい方を返すようにします。

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        
        def rob_helper(start: int, end: int) -> int:
            max_amount_robbed_previous = 0
            max_amount_skipped_previous = 0
            for i in range(start, end):
                new_robbed = max_amount_skipped_previous + nums[i]
                max_amount_skipped_previous = max(
                    max_amount_skipped_previous, max_amount_robbed_previous
                )
                max_amount_robbed_previous = new_robbed
            return max(max_amount_robbed_previous, max_amount_skipped_previous)

        return max(rob_helper(0, len(nums) - 1), rob_helper(1, len(nums)))

```

ネストが深くなったところに長い変数名が来ないようにしたいなと思いました。helper 関数を rob の外に出すことも考えます。
動的計画方でも書いてみようと思います。
max_money は i が、nums は start + i が走っていくので、リストを使って動的計画法を使うのであれば、rob_helper に nums をスライスしたものを渡した方が分かりやすいかもしれない。

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) <= 2:
            return max(nums)
        
        def rob_helper(start, end):
            # The range includes start but excludes end.
            size = end - start
            max_money = [0] * size
            max_money[0] = nums[start]
            max_money[1] = max(nums[start], nums[start + 1])
            for i in range(2, size):
                max_money[i] = max(max_money[i - 2] + nums[start + i], max_money[i - 1])
            return max_money[-1]

        return max(rob_helper(0, len(nums) - 1), rob_helper(1, len(nums)))

```

リストが空の場合に何を返すかの根拠ははっきりしていない。


## step2

https://github.com/sakupan102/arai60-practice/pull/37/files
	- 外側のリストと内側のリストの名前は変えておきたいと思った。

https://github.com/fhiyo/leetcode/pull/37/files
	- 区間をインデックスで表現する場合は、_rob_helper 内の early return を rob 関数でやっておきたい気持ちかも。
	
https://github.com/olsen-blue/Arai60/pull/36/files
	- 復習するときに改めて lru_cache の実装をやってみよう
    - スライスしたリストにどんな名前をつけるかは悩ましい。

helper 関数にリストを渡すことで少し読みやすくなった気がします。変数名も少し整理しました。

```python 

class Solution:
    def _rob_linearly_arranged_houses(self, nums: List[int]) -> int:
        max_amount_robbed = 0
        max_amount_skipped = 0
        for num in nums:
            new_robbed = max_amount_skipped + num
            max_amount_skipped = max(max_amount_skipped, max_amount_robbed)
            max_amount_robbed = new_robbed
        return max(max_amount_robbed, max_amount_skipped)

    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        return max(
            self._rob_linearly_arranged_houses(nums[:-1]),
            self._rob_linearly_arranged_houses(nums[1:]),
        )

```

## step3

練習していくうちに以下の形になりました。
rob_lineary_arranged_houses に区間をとるインデックスを渡す理由は、個人的に関数呼び出しで、スライスで指定するより見やすいと感じたからです。

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        def rob_lineary_arranged_houses(start: int, end: int) -> int:
            max_amount_robbed = 0
            max_amount_skipped = 0
            for i in range(start, end):
                new_robbed = max_amount_skipped + nums[i]
                max_amount_skipped = max(max_amount_skipped, max_amount_robbed)
                max_amount_robbed = new_robbed
            return max(max_amount_robbed, max_amount_skipped)

        return max(
            rob_lineary_arranged_houses(0, len(nums) - 1),
            rob_lineary_arranged_houses(1, len(nums)),
        )

```