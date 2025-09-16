# 35. Search Insert Position

## step1

ソートされているリスト nums を受け取り、中に target があればそのインデックスを返す。なければ、昇順を崩さずに挿入できるインデックスを返す。
リストの中を、target 未満の要素が並んだ区間と target 以上の要素が並んだ区間に分けて考えて、後者の区間の左端の要素のインデックスを返すとよさそうと思った。ただ、リストの要素がすべて target 未満の場合はリストの外側のインデックスを返すことになって、ここで頭の中が混乱した。

改めて考えてみると、すでに見つけた target 未満の要素が並んだ区間の末尾の次を指す変数 lower_bound と、すでに見つけた target 以上の要素が並んだ区間の先頭を指す変数 upper_bound を用意して、この二つの変数が示す探索空間が0になるまで小さくしていく作業を考えるのがよさそうだと思う。これなら lower_bound = 0 と upper_bound = len(nums) の初期化を自然に思える。

lower_bound を含まない左側にはこれまでに見つけた target 未満の要素があることを、upper_bound を含む右側にはこれまでに見つけた target 以上の要素があることを保証する。
lower_bound = 0, upper_bound = len(nums) で初期化することでどちらもまだ何もない状態で性質を保証していると考える。
middle を (lower_bound + upper_bound) で計算し、nums[middle] が target 未満の場合 [lower_bound, middle] の区間に target 以上の要素はないので、lower_bound を middle + 1 で更新してもよい。nums[middle] が target 以上の場合 [middle, upper_bound] の区間すべて target 以上の値のため upper_bound を middle で更新してもよい。
各探索で探索空間は一以上減るのでいずれ探索空間が0になってループが止まる。その時、lower_bound を含まない左側に target 未満の要素がすべてあるので、target が存在する場合は lower_bound に存在し、target が存在しない場合はこの位置に挿入する、と考えることで大丈夫そうだと思う。

```python

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        lower_bound = 0
        upper_bound = len(nums)
        while lower_bound < upper_bound:
            middle = (lower_bound + upper_bound) // 2
            if nums[middle] < target:
                lower_bound = middle + 1
            else:
                upper_bound = middle
        return lower_bound

```

upper_bound を含まない右側に、すでに見つけた target 以上の要素があることを保証する方法でもできそうだと思った。

```python

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        lower_bound = 0
        upper_bound = len(nums) - 1
        while lower_bound <= upper_bound:
            middle = (lower_bound + upper_bound) // 2
            if nums[middle] < target:
                lower_bound = middle + 1
            else:
                upper_bound = middle - 1
        return lower_bound

```

bisect — Array bisection algorithm: 
https://docs.python.org/3/library/bisect.html
https://github.com/python/cpython/blob/3.13/Lib/bisect.py

bisect_left と似ていると感じた。
return したいのが lower_bound なので、if で lower_bound else で upper_bound の更新をするので自然かなと思う。
この関数を使う人が区間を指定して使えるようにしたい場合のことを考えるのもいいですね。そうすると、区間の開始で負の値を指定されるのは不自然ですか。

## step2

- https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.c15qprmvxkc2
    - https://discord.com/channels/1084280443945353267/1192736784354918470/1199018938005213234
        > 左は含むが右は含まないつもりで書いているわけですね。left 以上 right 未満。
        > 「target はあるとすると、10以上10未満にあるんだよねー。」といったらそんな数はありません。
        - 直感的でわかりやすく感じる。
    - 次以降の問題を解きながら理解できているか確認していこう。

- https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.e13uiztrq2u9
    - https://github.com/Fuminiton/LeetCode/pull/41/files
        - 二分探索の問題を [false, false, ..., true, true, ..., true] に置き換えて考えるとのこと。今回の問題で言うと、len(nums) + 1 の長さのリストで考えるということかな。改めて整理しよう。

- https://github.com/TORUS0818/leetcode/pull/43
    > まずは「何を探しているのか」「ループごとに今どこまで分かっているのか」「それをどう変数に表現しているのか」というのが意味の部分の話で、あとはループの中で「終了条件」「更新」「必ず終了すること」という形式操作の話くらいです。
    - target と比較するところを関数に切り出すのもいいか。

- https://discord.com/channels/1084280443945353267/1200089668901937312/1214551909076176896
    > mid = (left + right) // 2
    > とすると、切り捨てられるので、
    > left <= mid < right
    > になります。
    - ここまでしっかり考えられてなかった。

- https://github.com/fhiyo/leetcode/pull/42/files
    - 今回の問題ではリストの中に重複が存在しないことになっているが、存在する場合は処理をどうするか意識しないといけないですね。

以下のように書いてみて、自分は二つの変数のことを境界と認識していると感じたので、step1 の方が意図にあっていると思いました。

```python

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left_index = 0
        right_index = len(nums)
        while left_index < right_index:
            middle = (left_index + right_index) // 2
            if nums[middle] < target:
                left_index = middle + 1
            else:
                right_index = middle
        return left_index

```

## step3

step1 と同じになりましたが、こちらで練習しました。

```python

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        lower_bound = 0
        upper_bound = len(nums)
        while lower_bound < upper_bound:
            middle = (lower_bound + upper_bound) // 2
            if nums[middle] < target:
                lower_bound = middle + 1
            else:
                upper_bound = middle
        return lower_bound

```