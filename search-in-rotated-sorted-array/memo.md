# 33. Search in Rotated Sorted Array

## step1

nums の中から target を探す。ない場合は -1 を返す。nums は rotated sorted されている。
まず、left と right を用意する。
    - left: ここより左側に target がないことを保証する
    - right: ここを含む右側に target がないことを保証する
target があるとすると left 以上 right 未満の場所にある。
調査対象の場所を middle とし、left <= middle < right を満たす場所を選べばいいので、(left + right) // 2 で計算する。調査対象の場所がなくなったときにループを終了したいので while を left < right とする。
nums[middle] を見つけたときの処理
    - target と等しい場合 middle を返す
    - nums[middle] が nums[-1] より大きい場合
        - [0, middle) の領域がソートされていることが分かるので、この領域に target が含まれているかどうか調べる
            - 含まれている場合: middle を含む右側に target がないことが分かるので、right を middle で更新する
            - 含まれていない場合: middle を含む左側に target がないことが分かるので、left を middle + 1 で更新する 
    - nums[middle] が nums[-1] 以下の場合
        - [middle, -1] の領域がソートされていることが分かるので、この領域に target が含まれているかどうか調べる（middle の場所にはないことが分かっている）
            - 含まれている場合: middle を含む左側に target がないことが分かるので、left を middle + 1 で更新する
            - 含まれていない場合: middle を含む右側に target がないことが分かるので、right を middle で更新する
どの場合も right を middle もしくは left を middle + 1 で更新しているので探索空間は必ず0になる。
もし target を見つけることなくループを終了した場合、-1 を返す。

```python

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums)
        while left < right:
            middle = (left + right) // 2
            if nums[middle] == target:
                return middle
            if nums[-1] < nums[middle]:
                if nums[0] <= target < nums[middle]:
                    right = middle
                else:
                    left = middle + 1
            else:
                if nums[middle] < target <= nums[-1]:
                    left = middle + 1
                else:
                    right = middle
        return -1

```

`if nums[0] <= target < nums[middle]:` の nums[0] は nums[left] でもよさそう
middle は left <= middle < left を満たす必要があり、middle + 1 して left になると配列外参照にならないようにする

right を、ここより右の領域に target がないことを保証するように意味を変えて書いてみる

```python

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            middle = (left + right) // 2
            if nums[middle] == target:
                return middle
            if nums[middle] > nums[-1]:
                if nums[0] <= target < nums[middle]:
                    right = middle - 1
                else:
                    left = middle + 1
            else:
                if nums[middle] < target <= nums[-1]:
                    left = middle + 1
                else:
                    right = middle - 1
        return -1

```

if 文を減らしたい気がする。


## step2

- https://github.com/saagchicken/coding_practice/pull/9/files
    - target を探すというよりは、この領域は、target が存在することができる領域かどうかを調べて、その領域を小さくしていくようなイメージを持ちました。

- https://discord.com/channels/1084280443945353267/1366778718705553520/1424810480479899762
    > まとめると、 nums[0] 以上 -2 target 未満 -1 targetと同じ 0 target より大 +1 nums[0] 未満 +2 の和を計算して、-2 か +2 かを探せばよいのかしら。
    - このあたりからわからなくなった。

- https://github.com/Ryotaro25/leetcode_first60/pull/47/file 
    - pivot を探す方法というやつは、二種類の二分探索を書いている。FindMinIndex 関数にも left と right を渡すようにしたいかも。
    - 関数に渡された left と right はそれだけ見るとわかりにくいので、saagachichen さんのように left_closed や right_closed のように書くといいかも。それかコメントを残すか。
    > これはたぶん、「可能性があるということを念頭に置いて下を書いた」ということなんでしょうが、どちらかというと知りたいのは「left, right」はそれぞれどういう数字なのか、ということです。
        - そうか、「この領域にあるかもしれない」という情報は、「この領域以外にないことを保証している」情報ではないわけで、だとすると、確かに後者の情報をコメントなどに明示した方が親切かも。意識できていなかった。

- https://github.com/Yoshiki-Iwasa/Arai60/pull/36
    - 自分の step1 のコードの外側の if else を `nums[left] <= nums[mid]` にすることもできますね。

saagchicken さんの書いたコードを参考にしました。
left は、ここより左側に target がないことを、right は、ここより右側に target がないことを保証している。
リストの中に一つだけ残した状態でループを終わるなら閉区間の方が自然かな。

```python

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if not nums:
            return -1

        def can_target_exist_in_range(left, right):
            # The target does not exist before index 'left'
            # The target does not exist after index 'right'
            if nums[left] <= nums[right]:
                return nums[left] <= target <= nums[right]
            else:
                return nums[left] <= target or target <= nums[right]

        left = 0
        right = len(nums) - 1
        while left < right:
            middle = (left + right) // 2
            if can_target_exist_in_range(left, middle):
                right = middle
            else:
                left = middle + 1
        
        if nums[left] == target:
            return left
        return -1

```

## step3

関数の引数の left と right は変えた方がいいと思うけどいい案が思いつかなかったので改めて考えます。

```python

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def can_target_exist_in_range(left, right):
            # The target does not exist outside the range [left, right].
            if nums[left] <= nums[right]:
                return nums[left] <= target <= nums[right]
            else:
                return nums[left] <= target or target <= nums[right]

        left = 0
        right = len(nums) - 1
        while left < right:
            middle = (left + right) // 2
            if can_target_exist_in_range(left, middle):
                right = middle
            else:
                left = middle + 1
        
        if nums and nums[left] == target:
            return left
        return -1

```
