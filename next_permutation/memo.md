# 31. Next Permutation

## step1

与えられたリストを in place で next permutation にする。
next permutation とは、すべての順列が自書式順序で並んでいるときの次の順列のこと。もし自書式順序において最後の順列が入力で与えられたときは先頭の順列(昇順に並んだ)とする。

制約:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100

辞書式順序における次の順列であるとはどういうことか考えてみる。リストの末尾が右端になり、降順になっている区間の左端を見つける。区間の左隣に要素があれば、その要素に対して区間の中から辞書順において次にくる要素と交換する。最後に、見つけた区間を昇順にすることで次の順列になると思う。

テストケース:
- [1, 2, 3]         ->  [1, 3, 2]
- [3, 2, 1]         ->  [1, 2, 3]
- [2, 2, 1]         ->  [1, 2, 2]
- [3, 5, 3, 1]      ->  [5, 1, 3, 3]
- [1, 1]            ->  [1, 1] (順列がそもそも一つしかない)
- [1]               ->  [1]

```python

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        left = 0
        for i in range(len(nums) - 1, 0, -1):
            if nums[i - 1] < nums[i]:
                left = i
                break

        if left != 0:
            for i in range(len(nums) - 1, left - 1, -1):
                if nums[left - 1] < nums[i]:
                    nums[left - 1], nums[i] = nums[i], nums[left - 1]
                    break

        right = len(nums) - 1
        for i in range((right - left + 1) // 2):
            nums[left + i], nums[right - i] = nums[right - i], nums[left + i]

```

最初にやりたいことはスワップなのでスワップ対象となるインデックスを探すところから始めた方が素直かもしれないか。あと、処理を関数化しながら考えた方がよさそう。。。

```python

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        def find_first_decreasing_from_right():
            for i in reversed(range(len(nums) - 1)):
                if nums[i] < nums[i + 1]:
                    return i
            return -1 # not found
        
        def find_lexicographic_successor(pivot, start):
            for i in reversed(range(start, len(nums))):
                if nums[i] > nums[pivot]:
                    return i

        def reverse_in_range(start, end):
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1
            
        left = find_first_decreasing_from_right()
        if left != -1:
            right = find_lexicographic_successor(pivot=left, start=left + 1)
            nums[left], nums[right] = nums[right], nums[left]

        reverse_in_range(left + 1, len(nums) - 1)

```

## step2

- https://github.com/fhiyo/leetcode/pull/56/files
    - left と right を見つける処理を分けずに、二重ループにするというのも見通しが良くていいかもしれない。
    - right を探索する範囲は降順にソートされた状態なので bisect も使える。
    - 今回は for ではなく while でもいいかもしれない。

- https://github.com/olsen-blue/Arai60/pull/59/files
    - reversed と range どっちがよみやすいかな。
    - swap する対象の変数名は left right が個人的に読みやすい気がするけど、pivot_index も実態を反映している気がしていいと思うし変数名いろいろと迷うな。

- https://github.com/tokuhirat/LeetCode/pull/58/files
    - `def rfind_successor(pivot_index: int) -> int:` のように pivot_index だけ渡して後ろから見ていくのもいい。

- https://discord.com/channels/1084280443945353267/1201211204547383386/1232011836543467660
    - https://discord.com/channels/1084280443945353267/1225849404037009609/1232410562454093866
    - https://discord.com/channels/1084280443945353267/1199984201521430588/1334835381782183988
    - https://en.cppreference.com/w/cpp/algorithm/next_permutation.html
    - cpp の実装。first と last という名前で範囲を指定するのは初めて見たかもしれない。いろいろあるんですね。
- https://discord.com/channels/1084280443945353267/1237649827240742942/1353878925117227113
    - 初期化の仕方について。読み方を参考にして自分も気をつけよう。
- https://discord.com/channels/1084280443945353267/1322513618217996338/1358693238290251788
    > 平均計算量は、可能な全入力に対しての平均です。たとえば、クイックソートならば、全順列を入れてみて平均を取ります。
    > 償却計算量は、ある最悪な入力の列に対しての振る舞いのことです。
    - 具体例見つけて整理する。

str と bytes には rfind がある: 
- https://docs.python.org/3/library/stdtypes.html#str.rfind
- https://docs.python.org/3/library/stdtypes.html#bytes.rfind

step1 の改善

```python

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        def find_first_decreasing_from_right():
            for i in reversed(range(len(nums) - 1)):
                if nums[i] < nums[i + 1]:
                    return i
            return -1 # not found
        
        def find_lexicographic_successor_to_right(pivot_index):
            for i in reversed(range(pivot_index + 1, len(nums))):
                if nums[i] > nums[pivot_index]:
                    return i

        def reverse_in_range(start, end):
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1
            
        pivot_index = find_first_decreasing_from_right()
        if pivot_index != -1:
            successor_index = find_lexicographic_successor_to_right(pivot_index)
            nums[pivot_index], nums[successor_index] = nums[successor_index], nums[pivot_index]

        reverse_in_range(pivot_index + 1, len(nums) - 1)

```

`def find_lexicographic_successor_to_right(pivot_index)` 関数に範囲を渡すのは余計複雑になるのかな。to_right が苦し紛れになっている気がして何とかしたいな。

ちょっと冗長かもしれないけどこっちの方がよさそうか。
`Elements from nums[pivot_index + 1] to the end are in decreasing order.`
`It is guaranteed that nums[pivot_index + 1] is greater than nums[pivot_index].`

## step3

最初は range の範囲を考えて reversed する方が書きやすいと思ったけど、読むときは range の方が読みやすい気がしてきました。
swap は個人的に欲しいと思ったけど、書いてる人見なかったのでどうだろうか。

この形で練習しました。

```python

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        def find_pivot():
            # Find the first index from the right where nums[i] < nums[i + 1].
            for i in range(len(nums) - 2, -1, -1):
                if nums[i] < nums[i + 1]:
                    return i
            return -1 # not found
        
        def find_successor(pivot_index):
            # Elements from nums[pivot_index + 1] to the end are in decreasing order.
            # It is guaranteed that nums[pivot_index + 1] is greater than nums[pivot_index].
            for i in range(len(nums) - 1, pivot_index, -1):
                if nums[i] > nums[pivot_index]:
                    return i

        def swap(left, right):
            nums[left], nums[right] = nums[right], nums[left]

        def reverse_in_range(start, end):
            while start < end:
                swap(start, end)
                start += 1
                end -= 1

        pivot_index = find_pivot()
        if pivot_index != -1:
            successor_index = find_successor(pivot_index)
            swap(pivot_index, successor_index)

        reverse_in_range(pivot_index + 1, len(nums) - 1)

```