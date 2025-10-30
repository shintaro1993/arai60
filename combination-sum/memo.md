# 39. Combination Sum

## step1

与えられた candidates を使って、和が target になるすべての組み合わせを返す。candidates の各要素は何回でも使ってよい。

探索の状態を木構造として考える。各ノードでは、現在までに選んだ要素のリスト、それらの和、次に選択する要素の開始インデックスを管理し、現在のインデックスから最後までの要素を選ぶ場合で分けて次の状態に進む。

```python

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []

        def get_combination_sum(selected_nums, total, start):
            if total > target:
                return
            if total == target:
                result.append(selected_nums)
                return
            
            for i in range(start, len(candidates)):
                num = candidates[i]
                get_combination_sum(selected_nums + [num], total + num, i)

        get_combination_sum([], 0, 0)
        return result

```

気になった点：
- 引数で total を渡していくより都度 sum で和をとった方が分かりやすいか、get_combination_sum 関数の最初の呼び出しでキーワードをつけたりコメントを書いたりするか。
- num より candidate の方がいいか。

上記イメージのままループで書く

```python

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        combinations_with_indices = [([], 0)]
        while combinations_with_indices:
            combination, start = combinations_with_indices.pop()
            total = sum(combination)
            if total > target:
                continue
            if total == target:
                result.append(combination)
                continue
            for i in range(start, len(candidates)):
                combinations_with_indices.append((combination + [candidates[i]], i))
        return result

```

n = len(candidates)
時間計算量は n * n^(target/min(candidates)) くらいとすると、30 * 30^(40/2) になるのかな。
紙に木を書いてみると枝に偏りがあるのが分かるけど、どんな感じで抑えれるのかわからない。。

## step2

- https://github.com/Mike0121/LeetCode/pull/1/files
    - 気持ちとしては、同じ要素を選べるまで選んで、その要素を選べなくなったら次の要素に移る、みたいな感じかな。これは range で candidates の長さを指定していないので if 文で制御しているのかな。
    - 時間計算量は、N-ary 木で考えるとわかるらしい: https://github.com/Mike0121/LeetCode/pull/1/files#r1578068513
        - 分割数についても見ておく: https://github.com/Mike0121/LeetCode/pull/1/files#r1578212926
 
- https://github.com/olsen-blue/Arai60/pull/53/files
    - 考え方としては Mike0121 さんと似てるのかな。わかりやすい気がする。
    - DP でもできるんですね。sum_combinations[sum_value] がリストで、そこに combination を append していくんですね。

- https://github.com/fhiyo/leetcode/pull/52/files
    - 先にソートして for 文の中で探索を打ち切るかどうか調べれば余計な探索をしなくてもよくなると。
    - そもそも探索を打ち切るかどうかや、結果に追加するかどうかのチェックをする場所もよく考えた方がいいな。

nums[i] を選ぶ場合と選ばない場合で分けて stack に積んでいくのもわかりやすいかと思ったが、木を書いてみると、step1 の方が自分にはわかりやすく感じた。
ただ他の状態遷移の考え方として参考になった。

```python

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        stack = [([], 0, 0)]
        while stack:
            combination, total, i = stack.pop()
            if i == len(candidates):
                continue
            if total > target:
                continue
            if total == target:
                result.append(combination)
                continue

            candidate = candidates[i]
            stack.append((combination + [candidate], total + candidate, i))
            stack.append((combination, total, i + 1))
        return result

```

step1 の修正。形が定まった感じがなかなかしない。

```python

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        stack = [([], 0, 0)]
        while stack:
            combination, total, start = stack.pop()
            if total == target:
                result.append(combination)
                continue

            for i in range(start, len(candidates)):
                candidate = candidates[i]
                if total + candidate > target:
                    continue
                stack.append((combination + [candidate], total + candidate, i))
        return result

```

## step3

3つ詰めたもののリストと2つ詰めたもののリストだと、スタックに対するイメージのしやすさが結構変わるなと思ったので total は取り出した後に計算するようにしました。

```python

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        combinations_with_indices = [([], 0)]
        while combinations_with_indices:
            combination, start = combinations_with_indices.pop()
            total = sum(combination)
            if total > target:
                continue
            if total == target:
                result.append(combination)
                continue

            for i in range(start, len(candidates)):
                combinations_with_indices.append((combination + [candidates[i]], i))
        return result

```