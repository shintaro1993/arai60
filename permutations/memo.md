# 46. Permutations

## step1

nums が与えられるので、すべての permutation を作って返す。
nums の長さは1以上6以下であり、すべての要素が異なっている場合について考える。

選び方は n 通り、n - 1 通り、n - 2 通り、...、1 通りと減っていく。すべての選び方を試せば作れそう。

```python

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []

        def permute_helper(permutation):
            if len(permutation) == len(nums):
                result.append(list(permutation))
                return
            for num in nums:
                if num in permutation:
                    continue
                permutation.append(num)
                permute_helper(permutation)
                permutation.pop()

        permute_helper([])
        return result

```

n = len(nums) とすると permute_helper は n! くらい呼び出されて、その中で for num in nums と list(permutation) や if num in permutation をやっていて、だいたい O(n! * n^2) くらいかな。n = 6, python で 1秒間に100万ステップ処理できるとすると、だいたい0.03秒くらいかな。

https://docs.python.org/3/library/itertools.html#itertools.permutations
ライブラリの方では、空のリストを与えると空のタプルが返ってくる。
ただし、今回の問題では戻り値が List[List[int]] のように指定されているのでどうするのか悩む。 

ループのイメージができてきたのでループでも書いてみる。

```python

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        permutations = [[]]
        while permutations:
            permutation = permutations.pop()
            if len(permutation) == len(nums):
                result.append(permutation)
                continue
            for num in nums:
                if num in permutation:
                    continue
                permutations.append(permutation + [num])
        return result

```

permutations の初期値を空のリストにしているのは突然だろうか。
permutation の更新方法はこっちが自然な気もする。

## step2

- https://github.com/tokuhirat/LeetCode/pull/50/files
    - 子の探索結果をリストに詰めて返せば、呼び出し元で返却用のリストを用意する必要がなくなりますね。
    - next_permutations などは、後の方で問題にあった気がするのでその時に見ておこう。
    - cycles の意味や全体の動きがいまいち理解できた気がしなかった。print 文挟みながらまた後で読んでみよう。

- https://github.com/olsen-blue/Arai60/pull/51
    - 残りの nums を管理するようにすると for 文 の中の if 文を取り除くことができますね。意味的には自然かもしれないけど、処理が分かりにくくなっている気もするので難しい。
    - permutation[:] でコピーを作る方がいいのかな。

- https://github.com/Ryotaro25/leetcode_first60/pull/54/files
    > あ、ここ nums で回しちゃうと、O(n! * n) の n が残っちゃうんですね。
    > ただ、変更しながらループで回すことはできないので、コピーすることになります。
    > それでも、最後の n はなくなります。
    - この辺の計算量の見積もりは理解がちょっと怪しいかも。
        - こっちも参考にして後で整理する: https://github.com/Fuminiton/LeetCode/pull/52#discussion_r2462737074

残っている nums を管理するとすると、以下の方法か、olsen-blue さんの PR で見たように、`next_rest_nums = rest_nums[:index] + rest_nums[index + 1:]` をして子に渡していくなどの方法があるのかな。
状況によってはこういうことを考えるときがくるということは思い出せるようにしておこう。

```python

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        remaining_nums = set(nums)

        def permute_helper(permutation):
            if len(permutation) == len(nums):
                result.append(list(permutation))
                return
            
            for num in list(remaining_nums):
                permutation.append(num)
                remaining_nums.remove(num)
                permute_helper(permutation)
                permutation.pop()
                remaining_nums.add(num)

        permute_helper([])
        return result

```

step1 の改善。リストの変数名を permutations にしていたけど、これはライブラリの permutations を想起させるかもしれないし変えるのもありかな。でも変数名が長くなるのもつらい。

```python

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        partial_permutations = [[]]
        while partial_permutations:
            permutation = partial_permutations.pop()
            if len(permutation) == len(nums):
                result.append(permutation)
                continue

            for num in nums:
                if num in permutation:
                    continue
                partial_permutations.append(permutation + [num])
        return result

```

## step3

step2 と同じ形で練習しました。

```python

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        partial_permutations = [[]]
        while partial_permutations:
            permutation = partial_permutations.pop()
            if len(permutation) == len(nums):
                result.append(permutation)
                continue

            for num in nums:
                if num in permutation:
                    continue
                partial_permutations.append(permutation + [num])
        return result

```