# 1. Two Sum

## Step1

- リストの中から、合計が target と一致する二つの数値を探し、それらのインデックスを返す。

- 二つの数値を探す方法として、リスト内を二重ループで探索する方法と、辞書を使ってペアを探す方法を考えました。

### 実装

- 二重ループを使う方法

- 見積り：
    - 時間計算量：O(n^2)
    - 空間計算量：O(1)

```python

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

```

- range 関数のかわりに enumerate を使う方法

- 見積り
    - 時間計算量：O(n^3)
    - 空間計算量：O(1)

- range 関数と似ているようで違うので少し注意。スライスのせいで少し読みにくい気もします。スライスをすることで O(n^3) くらいになると思います。
    - https://docs.python.org/3/library/functions.html#enumerate

```python

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i, num1 in enumerate(nums):
            for j, num2 in enumerate(nums[i + 1:], start=i + 1):
                if num1 + num2 == target:
                    return [i, j]
        return []

```

- 辞書を使って見つけた値とインデックスをメモしていく方法

- 見積り
    - 時間計算量：O(n)
    - 空間計算量：O(n)

```python

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [i, num_to_index[complement]]
            num_to_index[num] = i
        return []

```

- ここまで20分くらいです。

- 二つの値が見つからない場合と、あとはリストが空の場合と要素を一つしか持たない場合に、見つからなかったことをどのようにユーザーに報告するか考えます。

- str.find() では、見つからない場合は-1を返しています。
    - https://docs.python.org/3/library/stdtypes.html#str.find
- str.index() では、見つからない場合は ValueError を投げています。
    - https://docs.python.org/3/library/stdtypes.html#str.index
- list についても s.index() で要素が見つからない場合は ValueError を投げるそうです。
    - https://docs.python.org/3/library/stdtypes.html#common-sequence-operations

- https://docs.python.org/3/library/exceptions.html#ValueError
- https://google.github.io/styleguide/pyguide.html#24-exceptions

- 具体例少ないですが標準型の関数を見ると ValueError を投げるのが足並みそろっているかなと思いました。今回は戻り値の型を List[int] で想定されているのですが、そうでなければ None を返して、`if result is None` などで処理してもらうのでもいいかと思いました。ただ、戻り値は list を想定していますが実際は二つのインデックスを返すので、`i, j = twoSum(nums, target)` のような使い方をされたときのことまで考えるとどうするのがいいか迷います。今回は List 型が返るということが想定されているので、ValueError を投げる寄りになりました。

```python

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [i, num_to_index[complement]]
            num_to_index[num] = i
        
        raise ValueError("could not find two numbers.")

```

- complement を使わない方がメモから探すという動作においてわかりやすいが、メモをするということを考えるともう片方を使ってメモから探しておいた方がわかりやすい。

```python

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}
        for i, num in enumerate(nums):
            if num in num_to_index:
                return [i, num_to_index[num]]
            num_to_index[target - num] = i
        
        raise ValueError("could not find two numbers.")

```

## Step2

### 調べたこりコードを読んだりする

- https://github.com/takumihara/leetcode/pull/1/files
    - [-1, -1] を返す手もある。
    - この練習を始めてから辞書を使うときに `num_to_index` のような形式を使うことを自然だと感じるようになったが、nodchip さんが `チーム内で合意形成が得られれば`と言われているように、あくまで合意形成が得られればということを忘れないようにしないといけない。
- https://github.com/fhiyo/leetcode/pull/14/files
    - never reached のコメントを残すのは少し違和感があるかもしれない
- https://github.com/cheeseNA/leetcode/pull/1/files
    - リストをソートし、二つのポインタを使っている実装は思いつきませんでした。ソート前とソート後のインデックスの対応関係を保存しておく必要があるみたいです。復習するときに実装してみよう。
- https://github.com/Kitaken0107/GrindEasy/pull/4/files
    - 二回ループを回すことにはなるけど、メモ用のループと調べる用のループを分けるのも意外と負担なく読めた。
- https://github.com/nozomi-iida/arai60/pull/1/files
    - rust の panic というのは、Python の exit() のようなものでしょうか。想定はしていませんでした。
    - コメント集にリンクをまとめていただいていたので、改めて整理しよう
        - https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.jdtk9v35bca4
- https://github.com/huyfififi/coding-challenges/pull/1/files
    - セイウチ演算子は試したことがなかったのでどこかで試してみよう

- ループ内で num を持っている人が、相方のインデックスを探すときに使う辞書、という意味を込めて num_to_pair_index にしようと思いました。

```python

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_pair_index = {}
        for i, num in enumerate(nums):
            if num in num_to_pair_index:
                return [i, num_to_pair_index[num]]
            num_to_pair_index[target - num] = i
        
        raise ValueError("could not find two numbers.")

```

## Step3

- step2 のコードで書きあげる練習をしました。

## 感想

- 自分が不自然さを感じる原因について自覚したこととして、手作業の動作をプログラムに変換したときに起こっているように感じました。Step2 でやったように、意図などを自然言語で表現したものをプログラムに変換すると自分の中の不自然さが和らいでいるように感じました。手作業 -> 自然言語で説明 -> コンピュータにお願い、のステップを改めて意識しようと思います。
