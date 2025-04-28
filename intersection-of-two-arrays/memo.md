# 349. Intersection of Two Arrays

## Step1

- 考えたこと
    - 二つのリストから重複を取り除き、nums2 に含まれる要素を見つけたら結果に追加するという作業を、すべての nums1 の要素に対して行う。

## Step2

## set とループを使う方法

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        num_set1 = set(nums1)
        num_set2 = set(nums2)
        result = []
        for num1 in num_set1:
            if num1 in num_set2:
                result.append(num1)
        return result

```

- n: nums1 の長さ
- m: nums2 の長さ

- 見積り
    - 時間計算量：O(n + m)
    - 空間計算量：O(n + m)

- set の intersection は `O(min(len(s), len(t)))` だったので、cpython を少しのぞいてみようと思います。
    - https://wiki.python.org/moin/TimeComplexity
- `PyAnySet_Check` で t が set かどうかを確認しているので、確かにその場合はできそうだなと思いました。
    - https://github.com/python/cpython/blob/1b7470f8cbff4bb9e58edd940a997a3647e285e4/Objects/setobject.c#L1416
    - もし set ではない場合は、min が max になるそうです。wiki の Notes にちゃんと `replace "min" with "max" if t is not a set` と書かれていました。


### intersection 関数を使う方法

- https://docs.python.org/3/library/stdtypes.html#frozenset.intersection

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        num_set1 = set(nums1)
        num_set2 = set(nums2)
        result = num_set1.intersection(num_set2)
        return list(result)

```

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        num_set1 = set(nums1)
        num_set2 = set(nums2)
        result = num_set1 & num_set2
        return list(result)

```

- __and__() が呼ばれている
    - https://docs.python.org/3/reference/datamodel.html#object.__and__

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        num_set1 = set(nums1)
        num_set2 = set(nums2)
        result = num_set1.__and__(num_set2)
        return list(result)

```

### intersection_update 関数を使う方法

- https://docs.python.org/3/library/stdtypes.html#frozenset.intersection_update

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = set(nums1)
        result.intersection_update(set(nums2))
        return list(result)

```

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = set(nums1)
        result &= (set(nums2))
        return list(result)

```

- __iand()__ が呼ばれている
    - https://docs.python.org/3/reference/datamodel.html#object.__iand__

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = set(nums1)
        result.__iand__((set(nums2)))
        return list(result)

```

- 二つ以上のリストの intersection をとるときに便利そうだと感じました。

### 発想を調べる・コードを読む

- https://github.com/shining-ai/leetcode/pull/13/files
    - 最初に考えたことは似ているなと感じた。そのあと、ソートする方法については考えられなかったので、その方法で実装してみる。
- https://github.com/katataku/leetcode/pull/12
    - 追加の質問を自分で考えられるようにする
        > - 片方がとても大きくて、片方がとても小さいときには、大きい方を set にするのは大変じゃないでしょうか、特に大きいほうが sort 済みのときにはどうしますか。
        > - 他、両方ソートされていてとても大きければ、マージソートの変形のように書くと思います。
        > - 要するにこの問題の推定される出題意図は条件を変えたときに案がいくつか出てくるかです。
- https://github.com/aoshi2025s/leetcode-review/pull/2#discussion_r1900773670
    - 空間計算量を小さく抑える方法も考える
- https://github.com/quinn-sasha/leetcode/pull/13#discussion_r1960884543
    > 解けた後に、いくつか追加の条件が出てきて、その下でのアルゴリズムとそれらの pros and cons が要求されると思います。
- https://github.com/nittoco/leetcode/pull/15/files
    - 自分が読むときは element という変数名を素通りしましたが、情報の多さを気にしていると他の案を提案できるんだなと感じた。
- https://github.com/Mike0121/LeetCode/pull/30/files
    - 返却用のリストの名前が common だと、頭の中で come on を連想してしまうため、common_nums の方が分かりやすく感じた。
- https://github.com/kazukiii/leetcode/pull/14/files
    - `return list(set(nums1) & set(nums2))` の書き方と変数に置く書き方の両方の意見にわかれます。

- 考える流れとして、まず最初に整理した条件でコードを書くことまではまあよくて、その後「追加の条件」を考えるときに混乱しないようにしないとなあ。条件が同じで、「発想」が異なるものを考えることとごっちゃにならないように気をつけよう。

### サイズが大きくソート済みのリストと、サイズが小さなリストが与えられた場合

- LeetCode 上では動きません
- nums1 がソート済みのリストとである仮定しています。

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = set()
        for num2 in nums2:
            index1 = bisect.bisect_left(nums1, num2)
            if num2 == nums1[index1]:
                result.add(num2)
        return list(result)

```

- 見積り
    - 時間計算量：O(n log m)
    - 空間計算量：O(min(n, m)) （追加で使うメモリ）

### 両方ともサイズが大きいが、両方ともソートされている場合

- LeetCode 上では動きません
- nums1 と nums2 がソート済みのリストであると仮定しています。

- 記録として、一番最初に書いたものから少しずつ変化させていったものをのせています。

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = set()
        index1 = 0
        index2 = 0
        while index1 < len(nums1) and index2 < len(nums2):
            if nums1[index1] == nums2[index2]:
                result.add(nums1[index1])
                index1 += 1
                index2 += 1
                continue
            if nums1[index1] < nums2[index2]:
                index1 += 1
                continue
            if nums1[index1] > nums2[index2]:
                index2 += 1
                continue
        return list(result)

```

- result への追加処理を下におろしました。一回目書くときは一番上に置いておきたいのに、それ以降は下に置いておきたい気持ちになるもの不思議なものだなと思いました。

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = set()
        index1 = 0
        index2 = 0
        while index1 < len(nums1) and index2 < len(nums2):    
            if nums1[index1] < nums2[index2]:
                index1 += 1
                continue
            if nums1[index1] > nums2[index2]:
                index2 += 1
                continue
            result.add(nums1[index1])
            index1 += 1
            index2 += 1
        return list(result)

```

- result に追加してもいいかを調べることで、result をリストにしました。

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = []
        index1 = 0
        index2 = 0
        while index1 < len(nums1) and index2 < len(nums2):   
            if nums1[index1] < nums2[index2]:
                index1 += 1
                continue
            if nums1[index1] > nums2[index2]:
                index2 += 1
                continue
            if not result or nums1[index1] != result[-1]:
                result.append(nums1[index1]) 
                continue
            index1 += 1
            index2 += 1
        return result

```

- ループの中心となる作業が if 文の中にあることに違和感を感じて無理やり外に出しました。

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = []
        index1 = 0
        index2 = 0
        while index1 < len(nums1) and index2 < len(nums2):   
            if nums1[index1] < nums2[index2]:
                index1 += 1
                continue
            if nums1[index1] > nums2[index2]:
                index2 += 1
                continue
            if result and nums1[index1] == result[-1]:
                index1 += 1
                index2 += 1
                continue
            result.append(nums1[index1]) 
            index1 += 1
            index2 += 1
        return result

```

- 追加した後にインデックスを進めておく方法もあるなと思いました。

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = []
        index1 = 0
        index2 = 0
        while index1 < len(nums1) and index2 < len(nums2):   
            if nums1[index1] < nums2[index2]:
                index1 += 1
                continue
            if nums1[index1] > nums2[index2]:
                index2 += 1
                continue
            num = nums1[index1]
            result.append(num) 
            while index1 < len(nums1) and nums1[index1] == num:
                index1 += 1
            while index2 < len(nums2) and nums2[index2] == num:
                index2 += 1
        return result

```

- ここまで、入力のリストがソートされていることを仮定して書いたので、そのままでは LeetCode 上で動きません。

- 見積り
    - 時間計算量：O(n + m)
    - 空間計算量：O(min(n, m)) （追加で使うメモリ）
    - ソートした場合
        - 時間計算量：O(nlogn + mlogm)
        - 空間計算量：O(n + m)

- ※追記：入力に nan があるときに破綻するらしいので、考えながら後で戻ってくることにします。
    - https://github.com/fhiyo/leetcode/pull/16/files
    - https://discuss.python.org/t/nan-breaks-min-max-and-sorting-functions-a-solution/2868

### 空間計算量を O(min(n, m)) にしたい場合

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        if len(nums1) < len(nums2):
            nums1, nums2 = nums2, nums1
        num_set2 = set(nums2)
        result = []
        for num1 in nums1:
            if num1 in num_set2:
                result.append(num1)
                num_set2.remove(num1)
        return result

```

- 見積り
    - 時間計算量：O(max(n, m))
    - 空間計算量：O(min(n, m))

## Step3

- 普段他の言語を使われている方にも読みやすいのは、& よりも intersection かと思いこちらを選択しました。

```python

class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1_set = set(nums1)
        nums2_set = set(nums2)
        return list(nums1_set.intersection(nums2_set))

```

## 感想

- 一問30分くらい？で取り組めるようになるらしいが、その域はまだ先のように思う。自分は、自分にとって効果がある練習になるように、やり方など修正しながらやっていこうと思う。