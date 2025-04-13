# 20. Valid Parentheses

## Step1

- 考えたこと
    - 開きカッコと閉じカッコの正しい組を取り除いていき、最終的に何も残らなかったら、入力が有効であると判断してもよさそうだと理解しました。
    - 入力文字列を見て行く中で開きカッコを見つけたら保存して、閉じカッコを見つけたとき、対応する開きカッコがあるか調べようと思います。調べるときに必要な開きカッコは、一番最後に見つけたものだけなので、開きカッコの保存には stack を使おうと思います。
    - list の pop 操作が、最後の要素に対して平均 O(1) でできる
        - https://wiki.python.org/moin/TimeComplexity
    - collections の deque も使えそうだが、今回これを使うメリットがわからなかったので list を使います。あまり関係ないが、発音は deck らしい。

```python

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        open_to_close = {"(": ")", "{": "}", "[": "]"}
        for c in s:
            if c in "({[":
                stack.append(c)
                continue
            if not stack:
                return False
            last_open = stack.pop()
            if c != open_to_close[last_open]:
                return False
            
        return not stack

```

- 時間計算量：O(n)
- 空間計算量：O(n)
    - (((()))) などの場合に入力の半分の開きカッコが stack に保存される
- 15分くらいかかりました。

## Step2

### 調べたこと

- https://github.com/huyfififi/coding-challenges/pull/2/files
    - 辞書の key と value を縦に並べる書き方が思っているよりも見やすいと感じた
- https://github.com/plushn/SWE-Arai60/pull/6/files
    - 議論されているように、自分の場合、stack を open_brackets などにした方がわかりやすいなと感じた
    - stack と 辞書に番兵を入れておく方法があるらしいが、
    - 開きカッコを一か所にまとめておいた方が管理しやすいと思ったので、自分もそうしようと思う。
- https://github.com/BumbuShoji/Leetcode/pull/7/files
    - チョムスキー階層、タイプ-2、文脈自由文法、プッシュダウンオートマトンについては復習をするときに改めて調べようと思います。
- https://discord.com/channels/1084280443945353267/1225849404037009609/1231648833914802267
    > "(aiu)[eo]" が入力としてきたときに、プログラムの挙動として好ましいのは何だと考えますか?
    - プログラムの挙動として好ましいものという考えがなかった。考えてみると悩ましい。そもそもどのような関数にしましょうかという話をする段階では、この入力にも対応させた方がいいというかもしれない。関数の想定する入力がカッコのみの場合にこの入力が来たときの対応として、カッコ以外の文字が含まれていることをユーザーに伝えるのが正しいと思うかな（結果的にカッコの対応が正しくても間違っていても）。この点についてもこの練習を続けていく中で考えていきたい。


```python

class Solution:
    def isValid(self, s: str) -> bool:
        open_brackets = []
        brackets_pairs = {
            "(": ")", 
            "{": "}", 
            "[": "]",
        }

        for c in s:
            if c in brackets_pairs:
                open_brackets.append(c)
                continue
            if not open_brackets:
                return False
            last_open = open_brackets.pop()
            if c != brackets_pairs[last_open]:
                return False
            
        return not open_brackets

```

- stack の変数名を open_brackets にしようとしたが、そうすると、open_to_close と紛らわしいと思って少し悩む。

## Step3

- 以下のコードで0から書き上げる練習をしました。変数名については、復習をしたときに頭にすっと入ってきているかどうかなども参考に判断していきたい。

```python

class Solution:
    def isValid(self, s: str) -> bool:
        open_brackets = []
        bracket_pairs = {
            "(": ")",
            "{": "}",
            "[": "]",
        }

        for bracket in s:
            if bracket in bracket_pairs:
                open_brackets.append(bracket)
                continue
            if not open_brackets:
                return False
            last_open = open_brackets.pop()
            if bracket != bracket_pairs[last_open]:
                return False

        return not open_brackets

```