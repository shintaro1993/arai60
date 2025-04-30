# 387. First Unique Character in a String

## Step1

- 二回ループを回す方法を考えました。一回目で文字の個数をメモし、二回目で最初に見つけた個数が一個の文字のインデックスを返します。

- まずは辞書にメモする方法で書きます。

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        letter_to_count = {}
        for c in s:
            if c not in letter_to_count:
                letter_to_count[c] = 0
            letter_to_count[c] += 1
        for i, c in enumerate(s):
            if letter_to_count[c] == 1:
                return i
        return -1

```

- ループが二つあると、自分の好みで選択しにくく感じました。
- 最初のループ内の if 文をとってみます。

- 辞書の get 関数を使います。

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        letter_to_count = {}
        for c in s:
            letter_to_count[c] = letter_to_count.get(c, 0) + 1
        for i, c in enumerate(s):
            if letter_to_count[c] == 1:
                return i
        return -1

```

- defaultdict を使います。

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        letter_to_count = defaultdict(int)
        for c in s:
            letter_to_count[c] += 1
        for i, c in enumerate(s):
            if letter_to_count[c] == 1:
                return i
        return -1

```

- メモをリストに変更します。

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        letter_count = [0] * 26
        for c in s:
            letter_count[ord(c) - ord("a")] += 1
        for i, c in enumerate(s):
            if letter_count[ord(c) - ord("a")] == 1:
                return i
        return -1

```

- Counter を使って for 文を一つに減らすのも読みやすいです。

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        letter_to_count = Counter(s)
        for i, c in enumerate(s):
            if letter_to_count[c] == 1:
                return i
        return -1

```

- 二回目のループは入力文字列の長さだけ回していますが、今回有効な入力として想定しているのは英小文字だけなので、辞書を使ってループを回す方法も書いてみました。
- 一回目のループで文字をはじめて見つけたときに count を 1 で初期化して、それ以降に発見したときはデクリメントを続けていますが、もう少し何とかできそうな気がしています。

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        letter_to_count_and_index = {}
        for i, c in enumerate(s):
            if c not in letter_to_count_and_index:
                letter_to_count_and_index[c] = [1, i]
                continue
            letter_to_count_and_index[c][0] -= 1
        for count, index in letter_to_count_and_index.values():
            if count == 1:
                return index
        return -1

```

- 別の考え方として、ループの中で文字がユニークかどうか調べる方法でもできそうです。

- find 関数と rfind 関数を使って、インデックスを左端と右端から調べた結果が同じかどうかで判定することもできる。
- keyword arguments は受け付けないようです。
    - https://docs.python.org/3/library/stdtypes.html#str.find
    - https://docs.python.org/3/library/stdtypes.html#str.rfind

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        for i, c in enumerate(s):
            if s.find(c) == s.rfind(c):
                return i
        return -1  

```

- 想定しない文字を入力が含む場合、その文字のインデックスを返さないようにしようと思います。
- ord 関数を使っている実装では英小文字以外の文字が入ってきたときに配列外を参照してしまい、その他の実装では、英小文字以外のインデックスを返してしまうかもしれないですし、辞書を使う場合、サイズがどんどん大きくなってしまいます。

- そうすると if 文を二つ追加するのが自然な気がしますが、どうでしょうか。

```python

class Solution:
    def is_lowercase_english_letter(self, c: str) -> bool:
        return ord("a") <= ord(c) <= ord("z")

    def firstUniqChar(self, s: str) -> str:
        letter_to_count = {}
        for c in s:
            # 追加
            if not self.is_lowercase_english_letter(c): 
                continue
            if c not in letter_to_count:
                letter_to_count[c] = 0
            letter_to_count[c] += 1
        for i, c in enumerate(s):
            # 追加
            if not self.is_lowercase_english_letter(c):
                continue
            if letter_to_count[c] == 1:
                return i
        return -1

```

```python

class Solution:
    def is_lowercase_english_letter(self, c: str) -> bool:
        return ord("a") <= ord(c) <= ord("z")

    def firstUniqChar(self, s: str) -> str:
        letter_to_count = {}
        for c in s:
            # 追加
            if not self.is_lowercase_english_letter(c):
                continue
            if c not in letter_to_count:
                letter_to_count[c] = 0
            letter_to_count[c] += 1
        for i, c in enumerate(s):
            # 追加
            if c not in letter_to_count:
                continue
            if letter_to_count[c] == 1:
                return i
        return -1

```

## Step2

### 読んだコード

- https://github.com/su33331/practice/pull/2/files
    - 自分と同じで、(letter, character, c) の使い分けを悩んでおられるような気がする。自分が選ばない組み合わせが見れて参考になる。
- https://github.com/TORUS0818/leetcode/pull/17/files
    - 1-pass と呼ばれる方法があるが、辞書と集合を使う発想はなかったが、読んでみると複雑なことはしてない気がする。
- https://github.com/olsen-blue/Arai60/pull/15/files
    - 同じようなことを考えていると感じました。-1 の返し方についての議論もありました。
- https://github.com/t0hsumi/leetcode/pull/15/files
    - 冒頭で言われていますが、二重ループを使う方法も考えておきたかったです。LRU の実装をされていますね。こちらは宿題にしようと思います。
- https://github.com/fuga-98/arai60/pull/16/files
    - 再帰で書かれている方もいるようです。それ以外のコードは、似てきている印象です。

- https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0
    - 整理しておく

- 現状この形が読みやすいなと感じています。

```python

class Solution:
    def is_lowercase_english_letter(self, c: str) -> bool:
        return ord("a") <= ord(c) <= ord("z")

    def firstUniqChar(self, s: str) -> str:
        letter_to_count = defaultdict(int)
        for c in s:
            if not self.is_lowercase_english_letter(c): 
                continue
            letter_to_count[c] += 1

        for i, c in enumerate(s):
            if not self.is_lowercase_english_letter(c):
                continue
            if letter_to_count[c] == 1:
                return i
        return -1

```

- 見積り
    - n：s の長さ
    - 時間計算量：O(n)
    - 空間計算量：O(1) (追加で使う辞書のサイズを定数と考えたからです)

## Step3

- step2 のコードで書きました。

## 感想

- 新井さんの問題集の同じカテゴリで、比較する関数もなじみが出てきましたが、少し状況が変わると選択を悩むものなんだなと感じました。比較する習慣は続けていこうと思います。