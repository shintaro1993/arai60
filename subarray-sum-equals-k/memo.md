# 560. Subarray Sum Equals K

## Step1

- 考えたこと
    - 全ての subarray の和を計算しながら、それが k と等しいかどうか調べる

### 方法1

- 二重ループとスライスを使う方法を考えました。

- LeetCode 上では「Time Limit Exceeded」になります。

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                if sum(nums[i:j]) == k:
                    count += 1
        return count

```

- 見積り：
    - 時間計算量：O(n^3)
    - 空間計算量：O(n) 

- sum 関数は、引数で範囲の開始位置を指定できるのは知りませんでした。
    - https://docs.python.org/3/library/functions.html#sum

- スライスの方法として、itertools の islice も使えそうだと思いました。引数で負の値を使うと ValueError を出してくれるそうです。
    - https://docs.python.org/3/library/itertools.html#itertools.islice

### 方法2

- a[i:j+1] は a[i:j] に a[j] を足したものでなので、0で初期化した変数に、見つけた値を足し続けていくこともできると考えました。

- 見積り
    - 時間計算量：O(n^2)
    - 空間計算量：O(1)

- LeetCode 上では「Time Limit Exceeded」になります。

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_num = 0
        for i in range(len(nums)):
            accumulation = 0
            for j in range(i, len(nums)):
                accumulation += nums[j]
                if accumulation == k:
                    subarray_num += 1
        return subarray_num

```

- itertools の accumulate 関数も使えそうです。
    - https://docs.python.org/3/library/itertools.html#itertools.accumulate

- LeetCode 上では「Time Limit Exceeded」になります。

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_num = 0
        for i in range(len(nums)):
            for accumulation in accumulate(nums[i:]):
                if accumulation == k:
                    subarray_num += 1
        return subarray_num

```

- 先ほど確認した islice と組み合わせると、リストのコピーのためのコストを節約できそうです。先頭に `is` がついているので真理値を返しそうな雰囲気があるかもしれません。

- LeetCode 上では「Time Limit Exceeded」になります。

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_num = 0
        for i in range(len(nums)):
            for accumulation in accumulate(islice(nums, i, len(nums))):
                if accumulation == k:
                    subarray_num += 1
        return subarray_num

```

### 方法3

- ワンパスでできないか考えました。現在注目している要素で終わる subarray の中で、合計が k と等しくなるものを数えていこうと思いました。
- `先頭から現在注目している値までの範囲の合計 = 先頭から以前発見した、ある値までの範囲の合計 + k` という関係を考え、この関係を満たすような小さい方の範囲の合計を過去に発見していればカウントしてもよいと考えました。今回 nums の中には負の値も含まれているため、このような合計が複数あったときに対応するため、発見したものを辞書で管理しようと思います。

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_num = 0
        accumulation = 0
        prefix_sum_to_count = {accumulation: 1}
        for num in nums:
            accumulation += num
            complement = accumulation - k
            if complement in prefix_sum_to_count:
                subarray_num += prefix_sum_to_count[complement]
            if accumulation not in prefix_sum_to_count:
                prefix_sum_to_count[accumulation] = 0
            prefix_sum_to_count[accumulation] += 1
        return subarray_num

```

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_num = 0
        accumulation = 0
        prefix_sum_to_count = defaultdict(int)
        prefix_sum_to_count[accumulation] += 1
        for num in nums:
            accumulation += num
            complement = accumulation - k
            subarray_num += prefix_sum_to_count[complement]
            prefix_sum_to_count[accumulation] += 1
        return subarray_num

```

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        def count_subarray_sum_equals_to_k(prefix_sum):
            return prefix_sum_to_count[prefix_sum - k]

        subarray_num = 0
        prefix_sum_to_count = defaultdict(int, {0: 1})
        for prefix_sum in accumulate(nums):
            subarray_num += count_subarray_sum_equals_to_k(prefix_sum)
            prefix_sum_to_count[prefix_sum] += 1
        return subarray_num

```

- 見積
    - 時間計算量：O(n)
    - 空間計算量：O(n)

- 他の方がどのような変数名を付けているのか気になったので調べます。

## Step2

- https://github.com/plushn/SWE-Arai60/pull/16/files
    - 自分が書いた accumuration は、total にしてもよさそうです。
    - この資料も整理しておく
        - https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.bp0g0ai41eln
- https://github.com/irohafternoon/LeetCode/pull/18/files
    - 二重ループの回し方もいろいろあるようですね。left と right という名前がついていたのでわかりやすかったです。
- https://github.com/mura0086/arai60/pull/20/files
    - 日本語では累積和という言葉になるんですね。ループが二重になると、人によって書き方が変わって結構変わりますね。これなら伝わるだろうと思わないようにしていこうと思いました。
        - https://ja.wikipedia.org/wiki/%E7%B4%AF%E7%A9%8D%E5%92%8C
- https://github.com/fuga-98/arai60/pull/17/files
    - defaultdict の初期化を一行で書かれている人がいませんでしたが、二行に分けた方が読みやすいでしょうか
- https://github.com/Fuminiton/LeetCode/pull/16/files
    - step3 での空行の使い方が読みやすく感じました。ループの外に置く変数が多くなったらこのようにしてみようと思います。

- 結果として返す変数名に k を含めるか迷いましたが、result の方もいらっしゃいますし、バランスはとれているのかなと思いましたので、好みでこのままにしようと思います。

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        def count_subarray_sum_equals_to_k(prefix_sum):
            return prefix_sum_to_count[prefix_sum - k]

        subarray_num = 0
        prefix_sum_to_count = defaultdict(int, {0: 1})
        for prefix_sum in accumulate(nums):
            subarray_num += count_subarray_sum_equals_to_k(prefix_sum)
            prefix_sum_to_count[prefix_sum] += 1
        return subarray_num

```

## Step3

- 関数をなくすと、返却用の変数名を変えた方がいい気がしました。

```python

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_num_equals_to_k = 0
        prefix_sum_to_count = defaultdict(int, {0: 1})

        for prefix_sum in accumulate(nums):
            subarray_num_equals_to_k += prefix_sum_to_count[prefix_sum - k]
            prefix_sum_to_count[prefix_sum] += 1
        return subarray_num_equals_to_k

```
