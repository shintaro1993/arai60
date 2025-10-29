# 78. Subsets

## step1

ユニークな要素のリストが与えられる。それに対するすべての部分集合を返す。
リストの長さは1以上10以下を想定する。

すべての要素に対して選ぶ場合と選ばない場合がある。選ぶ場合と選ばない場合に分けて再帰的に処理をしていけば大丈夫そう。

```python

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []

        def subsets_helper(subset, remaining_nums):
            if not remaining_nums:
                result.append(subset)
                return
            
            num = remaining_nums[0]
            remaining_nums = remaining_nums[1:]
            subsets_helper(subset + [num], remaining_nums)
            subsets_helper(subset, remaining_nums)

        subsets_helper([], nums[:])
        return result

```

時間計算量：O(n*2^n) - n は 1以上10以下なので、ざっくりと0.01秒くらいで見ておくといいか
空間計算量：O(n*2^n)

subsets_helper 関数の中でスライスを使って remaining_nums を更新していて、これはインデックスを引き継いでく方法にもできそう。
一つ目の subsets_helper 関数の前後で append して pop することもできる。ただこの組み合わせだと同じ関数呼び出しになってなんかもやっとする。

```python

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []

        def subsets_helper(i, subset):
            if i == len(nums):
                result.append(subset[:])
                return
            
            subset.append(nums[i])
            subsets_helper(i + 1, subset)
            subset.pop()
            subsets_helper(i + 1, subset)

        subsets_helper(0, [])
        return result

```

ループで書こうと思ったとき、以下のような木を考えて、降りながら result に追加していくのもいいかなと思いました。

                             [ ]
                 /            |               \
               [1]           [2]              [3]
              /    \        /            
          [1,2]   [1,3]  [2,3]
          /   
     [1,2,3] 

```python

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        subsets_and_indices = [([], 0)]
        while subsets_and_indices:
            subset, start = subsets_and_indices.pop()
            result.append(subset)
            for i in range(start, len(nums)):
                subsets_and_indices.append((subset + [nums[i]], i + 1))
        return result

```

## step2

- https://github.com/goto-untrapped/Arai60/pull/39/files
    - bit 演算を使う方法もあるのですね。
        - 000 -> []
        - 001 -> [1]
        - 010 -> [2]
        - 011 -> [1, 2]
        - 100 -> [3]
        - 101 -> [1, 3]
        - 110 -> [2, 3]
        - 111 -> [1, 2, 3]
        - 順番逆ですが、ループの中で立っているビットを調べて、それを subset として結果に入れていく感じかな。

- https://github.com/fhiyo/leetcode/pull/51/files
    - step1 のループで書いたような考え方の気がしますが、二重ループで書くこともできるのですね。
    - 他にもいろいろあるようで後で見ておこう
        - https://github.com/fhiyo/leetcode/pull/51/files#r1690145563
        - https://github.com/fhiyo/leetcode/pull/51/files#r1690083436

- https://github.com/olsen-blue/Arai60/pull/52/files
    - ループの中で、その要素を選ぶ場合と選ばない場合に分けて stack に追加する方がなんだかんだわかりやすいかも。

二重ループで書く方法もよいかと思ったが、result を使ってループを回しているのが気になるかも。

```python

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = [[]]
        for num in nums:
            new_subsets = []
            for subset in result:
                new_subsets.append(subset + [num])
            result.extend(new_subsets)
        return result

```

選ぶか選ばないかを考えればいいので、step1 のループよりもこっちが好きかも。
木構造の問題をやっているときもそうだったけど、stack に乗せるものが増えてくると変数名が長くなったりしがちなので気を付けるようにする。

```python

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        subsets_and_indices = [([], 0)]
        while subsets_and_indices:
            subset, i = subsets_and_indices.pop()
            if i == len(nums):
                result.append(subset)
                continue
            subsets_and_indices.append((subset + [nums[i]], i + 1))
            subsets_and_indices.append((subset, i + 1))
        return result

```

## step3

この形で練習しました。

```python

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        subsets_with_indices = [([], 0)]
        while subsets_with_indices:
            subset, i = subsets_with_indices.pop()
            if i == len(nums):
                result.append(subset)
                continue
            subsets_with_indices.append((subset + [nums[i]], i + 1))
            subsets_with_indices.append((subset, i + 1))
        return result

```

