# 198. House Robber

## step1

nums[0] から nums[i] までを使ってできる最大値を計算していくことにするとよさそう。

n = len(nums)
時間計算量: O(n)
空間計算量: O(n)

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums)

        max_money_so_far = [0] * len(nums)
        max_money_so_far[0] = nums[0]
        max_money_so_far[1] = max(nums[0], nums[1])
        for i in range(2, len(nums)):
            max_money_so_far[i] = max(
                max_money_so_far[i - 1], max_money_so_far[i - 2] + nums[i]
            )
        return max_money_so_far[-1]

```

`if len(nums) == 1` と `if len(nums) == 2` について、max_money_so_far のサイズを + 2 すればループの中で処理できそうですがわかりにくくなりそうな気がします。
len(nums) は何度も出てくるので変数に置くのもいいかも。
max_money_so_far について、一度には直前二つしか使っていないのでリストを二つの変数に置き換えても大丈夫そう。

リストを変数二つに置き換えた方法で書く。
nums の i-1 番目まで使っていい場合の最大値と i-2 番目までを使っていい場合の最大値があり、それを更新していくとループが終った後 i-1 番目まで使っていい場合の最大値が全体の最大値になると考える。

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums)

        max_two_steps_before = nums[0]
        max_one_steps_before = max(nums[0], nums[1])
        for i in range(2, len(nums)):
            new_max_one_steps_before = max(
                max_one_steps_before, max_two_steps_before + nums[i]
            )
            max_two_steps_before = max_one_steps_before
            max_one_steps_before = new_max_one_steps_before
        return max_one_steps_before

```

## step2

### 調べたこと・読んだコード

- https://github.com/sakupan102/arai60-practice/pull/36/files
	- nums のサイズが1の場合と2の場合の処理はまとめられることまで意識できていなかった。そもそも nums のサイズが2の場合はしたと合流できることに気が付いていなかった。
	- 配列外参照を防ぐ目的の場合と、early return が目的の場合をもう少し区別して考えよう。

- https://github.com/YukiMichishita/LeetCode/pull/16/files
	- `max_2_days_ago` はわかりやすいかも。でもこれらを0で初期化はしない方がわかりやすいかな。
	- 変数二つを使う場合、返却用の変数を別で用意する方がわかりやすいかも？。

- https://github.com/fhiyo/leetcode/pull/36/files
	- サイズ2のリストを使うよりは変数二つ用意した方が読みやすいかな。
	- 再帰でも書けます。
	- so_far よりは最後を使うか使わないかという話も

- https://github.com/nittoco/leetcode/pull/39
	> 「伝言」の内容は「ここまで最大いくら取れる、俺の眼の前の家に盗みに入らないとすると最大いくら取れる」の二つだけじゃないですか。
	- 二つの変数を使う方法をリストを使う方法の延長線上で考えるのではなく、直前の人から「直前の人が盗んだ場合の最大値と盗まない場合の最大値」を渡してもらうと考えると、これだけで自然に考えられる。直前の人から skipped_previous と robbed_previous を受け取る。previous は、この情報を受け取った立場で考えるとある方が親切かなと思った。

step1 の改善をする

個人的には nums のサイズが2の場合もすぐに return しておきたいと感じる。

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) <= 2:
            return max(nums)

        max_money = [0] * len(nums)
        max_money[0] = nums[0]
        max_money[1] = max(nums[0], nums[1])
        for i in range(2, len(nums)):
            max_money[i] = max(
                max_money[i - 1], max_money[i - 2] + nums[i]
            )
        return max_money[-1]

```

二つの変数を使う方法も修正しました。
nums[i] 番目を使う場合の最大値と使わない場合の最大値を管理していく考えです。この方法だと二つの変数を0で初期化するのもいいかもしれない。
変数名はもう少し考えたいと思った。コメントをうまく使えないかな。

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        max_money_robbed_previous = 0
        max_money_skipped_previous = 0
        for num in nums:
            new_robbed = max_money_skipped_previous + num
            max_money_skipped_previous = max(
                max_money_skipped_previous, max_money_robbed_previous
            )
            max_money_robbed_previous = new_robbed
        return max(max_money_robbed_previous, max_money_skipped_previous)

```

メモ化再帰の練習。
計算結果を変数に置いた方がいいと思ったがどうだろうか。
i が0の場合と1の場合を再帰の外に出さない方が分かりやすいかな。

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_money = {}
        def rob_helper(i: int) -> int:
            if i == 0:
                return nums[0]
            if i == 1:
                return max(nums[0], nums[1])
            if i in max_money:
                return max_money[i]
            
            max_money[i] = max(rob_helper(i - 2) + nums[i], rob_helper(i - 1))
            return max_money[i]
        
        return rob_helper(len(nums) - 1)

```

## step3

以下のコードで練習しました。
`max_money_robbed` と `max_money_skipped` に一度しましたが、個人的には以下の方に戻りました。

```python

class Solution:
    def rob(self, nums: List[int]) -> int:
        max_amount_robbed_previous = 0
        max_amount_skipped_previous = 0
        for num in nums:
            new_robbed = max_amount_skipped_previous + num
            max_amount_skipped_previous = max(
                max_amount_skipped_previous, max_amount_robbed_previous
            )
            max_amount_robbed_previous = new_robbed
        return max(max_amount_robbed_previous, max_amount_skipped_previous)

```