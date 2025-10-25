# 3. Longest Substring Without Repeating Characters

## step1

文字列 s が与えられる。その中の重複がない最大の部分文字列の長さを返す。

i を 0 から len(s) - 1 までとして、s[i] が右端になる部分文字列の最大の長さをそれぞれ調べていき、その中の最大の長さを返すとよさそう。
i - 1 番目の人から引き継いでもらいたい情報として、s[i - 1] が右端になる重複のない最大の部分配列（この左端を start にしよう）とその文字列に含まれる文字の出現頻度の情報があるといいかな。i 番目の人は s[i] を追加して重複がなければ最大の長さを更新して、重複があれば重複がなくなるまで s[i] が右端になる部分文字列を小さくして次の人に引き継ぐ。

```python

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = 0
        frequency_count = defaultdict(int)
        start = 0
        for end in range(len(s)):
            frequency_count[s[end]] += 1
            while frequency_count[s[end]] == 2:
                frequency_count[s[start]] -= 1
                start += 1
            max_length = max(max_length, end - start + 1)
        return max_length

```

自然言語での説明と少し変わってしまった。

## step2

- https://github.com/Mike0121/LeetCode/pull/21/files
    - set を使って重複を管理する方が分かりやすいかも
    - 自分の frequency_count の使い方だとなんだかフラグのように扱っているようで、defaultdict じゃなくてもいいかもしれない

- https://github.com/tokuhirat/LeetCode/pull/48/files
    - 各文字のインデックスを管理することで、ループを回すことなく left を計算することもできるのですね。
    - left_index が後ろに戻らないために max する必要があることに気づくのが難しかった。
        > left_index = max(left_index, letter_to_index[s[right_index]] + 1)

- https://github.com/olsen-blue/Arai60/pull/49/files
    - get を使って条件分岐を回避する工夫もできるのですね。
        - https://docs.python.org/3/library/stdtypes.html#dict.get
    - 自分は set を使う方が考えやすいかな。

各文字のインデックスを管理して、それ利用して start を計算します。
enumerate を使った方が分かりやすい気がする。
https://docs.python.org/3/library/functions.html#enumerate

```python

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = 0
        letter_to_index = {}
        start = 0
        for end, letter in enumerate(s):
            if letter in letter_to_index:
                start = max(start, letter_to_index[letter] + 1)
            max_length = max(max_length, end - start + 1)
            letter_to_index[letter] = end
        return max_length

```

やっぱり、set を使った書き方が分かりやすいかも。
set の変数名は seen とはちょっと違う気がして悩みます。他の候補として、window などもよさそうと思いました。sliding window と言ったりもするのですかね。
    - https://github.com/olsen-blue/Arai60/pull/49/files#r2005197346

```python

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = 0
        letters_in_range = set()
        start = 0
        for end, letter in enumerate(s):
            while letter in letters_in_range:
                letters_in_range.remove(s[start])
                start += 1
            max_length = max(max_length, end - start + 1)
            letters_in_range.add(letter)
        return max_length

```

## step3

この形で練習しました。
step1 では end をループの最初で記録しましたが順番が変わりました。自然言語での説明の仕方とコードとの距離が遠くならないように意識していこうと思いました。

```python

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = 0
        letters_in_range = set()
        start = 0
        for end, letter in enumerate(s):
            if letter in letters_in_range:
                letters_in_range.remove(letter)
                start += 1
            letters_in_range[letter] = end
            max_length = max(max_length, end - start + 1)
        return max_length

```
