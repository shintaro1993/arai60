# 22. Generate Parentheses

## step1

n が与えられるので、n ペアの正しいカッコの組み合わせをすべて返す。

左のカッコと右の回ッコの選び方で n * 2 回選び続けて、2^(n*2) 個の組み合わせを作りそれが正しいかどうか調べる方法を考えたが、途中で正しくないことに気づいたらその場合を終わらせた方が自然だと思った。
今までに使った左のカッコの数(num_left)と右のカッコの数(num_right)を管理しながら処理を進める。左のカッコしか選べない場合は num_left == num_right の場合、右のカッコしか選べない場合は num_left == n の場合で、それ以外の場合はどちらでも選べる。

```python

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []

        def generate_parenthesis_helper(parenthesis, num_left, num_right):
            if num_left + num_right == n * 2:
                result.append("".join(parenthesis))
                return
            
            if num_left == num_right:
                generate_parenthesis_helper(parenthesis + ["("], num_left + 1, num_right)
                return
            if num_left == n:
                generate_parenthesis_helper(parenthesis + [")"], num_left, num_right + 1)
                return
            generate_parenthesis_helper(parenthesis + ["("], num_left + 1, num_right)
            generate_parenthesis_helper(parenthesis + [")"], num_left, num_right + 1)

        generate_parenthesis_helper([], 0, 0)
        return result

```

場合分けを変更する。
まず、num_left < n の場合左のカッコは選んでもよく、num_right < num_left の場合は右のカッコを選んでもよい、とする。

```python

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []

        def generate_parenthesis_helper(parenthesis, num_left, num_right):
            if num_left + num_right == n * 2:
                result.append("".join(parenthesis))
                return
            
            if num_left < n:
                generate_parenthesis_helper(parenthesis + ["("], num_left + 1, num_right)
            if num_right < num_left:
                generate_parenthesis_helper(parenthesis + [")"], num_left, num_right + 1)

        generate_parenthesis_helper([], 0, 0)
        return result

```

上記の再帰をループで書く。

```python

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        stack = [([], 0, 0)]
        while stack:
            parenthesis, num_left, num_right = stack.pop()
            if num_left + num_right == n * 2:
                result.append("".join(parenthesis))
                continue

            if num_left < n:
                stack.append((parenthesis + ["("], num_left + 1, num_right))
            if num_right < num_left:
                stack.append((parenthesis + [")"], num_left, num_right + 1))

        return result

```
n: 1 <= n <= 8
m: 2 * n
計算量は、O(2^m*m) くらいで考える。1秒間に100万ステップ処理できるとすると、ざっくり1秒くらいかな。
不正なカッコの組み合わせは保存しないので、実際はもう少し下に抑えられるのかな。

## step2

- https://github.com/fhiyo/leetcode/pull/53/files
    - 使える数の残りを管理する考えもある。left を追加できる場合については if left > 0 の方が分かりやすい気がする。if right - left > 0 はどうかな。変数名は少し変えたい。num_remaining_left とすると長いか。
    - left_open_count=0, right_rest_count=n でやっていくのはちょっと混乱するかも。open よりは used な気はする。
    - リストで持つか文字列で持つか。
    - cache を使って3重ループする方法もあるのですね。また後で読もう。
        - https://github.com/fhiyo/leetcode/pull/53/files#diff-9ca14f2eb9507a65f01cd60a9947537f09b5daeede1ef28ee1d790d8d76adb56R194
    - 計算量はカタラン数
        - https://github.com/fhiyo/leetcode/pull/53/files#diff-9ca14f2eb9507a65f01cd60a9947537f09b5daeede1ef28ee1d790d8d76adb56R11

- https://github.com/olsen-blue/Arai60/pull/54/files
    - ")" を追加するパターンを網羅するようにしているのかな。分類の仕方はいろいろあるということですね。
        - こっちも参照：https://discord.com/channels/1084280443945353267/1218823830743547914/1231546400714788864
    > はじめの括弧とそれに対応する括弧に注目して「(A)B」と分けるのも分類ですね。
    - 正しい場合は、どんなカッコの列でも「(A)B」のように分類できるということかな。コメントはあった方がよさそう。

- https://github.com/Yoshiki-Iwasa/Arai60/pull/58/files
    - rest_open_count という変数名好みかも。少し変えたいか。

左と右の、使える数の残りを管理するように修正。

```python

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        stack = [([], n, n)]
        while stack:
            parenthesis, num_rest_opens, num_rest_closes = stack.pop()
            if num_rest_opens == 0 and num_rest_closes == 0:
                result.append("".join(parenthesis))
                continue

            if num_rest_opens > 0:
                stack.append((parenthesis + ["("], num_rest_opens - 1, num_rest_closes))
            if num_rest_closes > num_rest_opens:
                stack.append((parenthesis + [")"], num_rest_opens, num_rest_closes - 1))

        return result

```

## step3

この形で練習しました。

```python

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        stack = [([], n, n)]
        while stack:
            parenthesis, num_rest_opens, num_rest_closes = stack.pop()
            if num_rest_opens == 0 and num_rest_closes == 0:
                result.append("".join(parenthesis))
                continue

            if num_rest_opens > 0:
                stack.append(
                    (
                        parenthesis + ["("],
                        num_rest_opens - 1,
                        num_rest_closes,
                    )
                )

            if num_rest_closes > num_rest_opens:
                stack.append(
                    (
                        parenthesis + [")"],
                        num_rest_opens,
                        num_rest_closes - 1,
                    )
                )

        return result

```