# 139. Word Break

## step1

辞書の単語を使って入力文字列を分割できるかどうか調べる（同じ単語を何度使ってもよい）

考えたこと:
- この問題では、どの単語を使ったかを覚えておく必要はない
- 左から分割していくとよさそうだが、分割の仕方によって後の分割に影響が出る
- 入力文字列の先頭から分割できる区間の情報をメモしながら更新していくとよさそう？どのように実装しようか考える
- m = 入力文字列、n = 辞書のサイズとすると、O(mn) くらいでできそうかな

```python

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        is_breakable = [False] * len(s)
        for stop in range(1, len(s) + 1):
            for word in wordDict:
                if s[0:stop].endswith(word):
                    if stop - len(word) == 0 or is_breakable[stop - len(word) - 1]:
                        is_breakable[stop - 1] = True
        return is_breakable[-1]

```

endswith: https://docs.python.org/3/library/stdtypes.html#str.endswith
ドキュメントを見ると `str[start:end].endswith(suffix)` のように書かれているので、右端を end で合わせようか。あと start で0を指定する必要はなかったし、インデックスは endswith に渡すこともできる。

文字列をスライスするためのインデックスと is_brekable のインデックスの関係を整理せずに書いてしまったのでわかりにくい。
先頭から右端(end)を含まない区間の文字列において、それを分割できるかどうかの情報を is_brekable[end] で管理していく。is_brekable[0] を True で初期化するが、空文字を分割できると考えることには違和感がある。

```python

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        is_breakable = [False] * (len(s) + 1)
        is_breakable[0] = True
        for end in range(1, len(s) + 1):
            for word in wordDict:
                if s.endswith(word, 0, end) and is_breakable[end - len(word)]:
                    is_breakable[end] = True
        return is_breakable[-1]

```

s が空の場合は wordDict の中の単語を使って分割しているとは言えないと思うので False を返すのが正しいと思うが、今のままだと True が返るので、関数の先頭でチェックして返すか他を変えるかかな。
この問題においては wordDict に重複がないということになっているが、重複がある場合を考えると set にしておく方が自然かも
end - len(word) の範囲チェックを追加して、条件を逆にした方がわかりやすいかな。

## step2

- https://github.com/hayashi-ay/leetcode/pull/61/files
    - 正規表現を使えるとは思いもしなかった。これはまた後で整理しよう。
    - top down dp でも書ける。
    - ボトムアップの書き方は自分と違って右からループを回しています。左からの方が考えやすいか。
    - 見つかったら break するのは確かに自然だと思った。

- https://github.com/shining-ai/leetcode/pull/39/files
    > あー、すみません。Python の正規表現エンジンは、DFA ではなくて NFA なので、
    - Python の正規表現についても調べよう。
    - ローリングハッシュなどもあるらしい。
    - 考え方に違うところはあるが、if 文を二行に分けるのもいいと思った。

- https://github.com/olsen-blue/Arai60/pull/39/files
    - なるほど、外側のループのインデックスを start と考えて、is_breakable[start + len(word)] を True にできるか調べていくこともできる。こちらもわかりやすいし書き換えがしやすそう。
    - 確かに、is_xxx は関数名にも見える。segmentables や index_to_segmentable などを参考にする。

- https://github.com/Fuminiton/LeetCode/pull/39/files
    - そうか、step1 のコードでも、startswith を使うことができるが、個人的には endswith の気持ちかも。

start でループを回して、[start, start + len(word)) の区間で分割できるところを探していく方針で書いてみる。
これは step1 で書いたのと違って、見つかったときに break すると s = "aba", wordDict = ["a", "ab"] のようなケースで落ちてしまう。
if not segmentables[start]: の部分はすこし違和感があるかも。

startswith: https://docs.python.org/3/library/stdtypes.html#str.startswith

```python

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        segmentables = [False] * (len(s) + 1)
        segmentables[0] = True
        for start in range(len(s)):
            if not segmentables[start]:
                continue
            for word in wordDict:
                if s.startswith(word, start):
                    segmentables[start + len(word)] = True
        return segmentables[-1]

```

step1 の改善をする。
step1 の if 文の条件は順番を変えた方が自然だと思ったので修正。今のところコメントもあった方が読みやすい気がしている。 
segmentables[0] の場合のこともコメントした方がいいかは迷うが、これで練習しよう。

```python

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        if not s:
            return False
        
        # True if s[0:i) can be segmented, otherwise False
        segmentables = [False] * (len(s) + 1)
        segmentables[0] = True
        for end in range(1, len(s) + 1):
            for word in wordDict:
                start = end - len(word)
                if start < 0 or not segmentables[start]:
                    continue
                if s.endswith(word, 0, end):
                    segmentables[end] = True
                    break
        return segmentables[-1]

```

## step3

ループのインデックスを end で回しているので、step1 のように書くのも選択肢としてなしではないような気もしてきましたが、ひとまずこの形に落ち着きました。

```python

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        if not s:
            return False
        
        # True if s[0, i) can be segmented, otherwise False
        segmentables = [False] * (len(s) + 1)
        segmentables[0] = True
        for end in range(1, len(s) + 1):
            for word in wordDict:
                start = end - len(word)
                if start < 0 or not segmentables[start]:
                    continue
                if s.endswith(word, 0, end):
                    segmentables[end] = True
                    break
        return segmentables[-1]

```