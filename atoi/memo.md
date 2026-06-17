# 8. String to Integer (atoi)

## step1

与えられた文字列を32ビット符号付き整数に変換する関数を作る。

要件:
1. 先頭の空白を無視する。
2. '-' は負の値として、'+' と何もない場合は正の値として扱う。
3. 先頭の0はは無視する。数字以外の文字を発見するか入力がなくなるまで読む。数字がない場合は0を返す。
4. 結果を、[-2^31, 2^31 - 1] の範囲に収める。

テストケース:
- " 1" -> 1
- "1" -> 1
- "-1" -> -1
- "+1" -> 1
- "+001" -> 1
- "1a3" -> 1
- "-2147483649" -> -2147483648
- "+2147483648" -> 2147483647
- "00+1" -> 0
- " " -> 0
- "" -> 0
- "a" -> 0
- "0" -> 0

制約:
- 0 <= s.length <= 200
- s は、English letters (lower-case and upper-case), digits (0-9), ' ', '+', '-', and '.' で構成される

一文字ずつ調べながら要件通りの処理をしていけば大丈夫そう。

```python

class Solution:
    def myAtoi(self, s: str) -> int:
        i = 0
        while i < len(s) and s[i] == " ":
            i += 1

        sign = 1
        if i < len(s) and s[i] in "+-":
            if s[i] == "-":
                sign = -1
            i += 1

        result = 0
        while i < len(s) and s[i].isdigit():
            result = (result * 10) + int(s[i])
            i += 1

        result *= sign
        result = max(result, -2 ** 31)
        result = min(result, 2 ** 31 - 1)
        return result

```

時間計算量: O(n)
空間計算量: O(1)

- https://en.cppreference.com/w/cpp/string/byte/atoi.html
    - INT_MIN や LONG_MIN をサポートするために -= digit している
- https://docs.python.org/3/library/stdtypes.html#str.isspace
- https://docs.python.org/3/library/stdtypes.html#str.isdigit
- https://docs.python.org/3/library/string.html#string.digits
- https://docs.python.org/3/library/stdtypes.html#str.lstrip
- https://docs.python.org/3/library/stdtypes.html#str.startswith
- https://docs.python.org/3/library/functions.html#int
- https://docs.python.org/3/library/functions.html#ord

調べてみたら lstrip や startswith, removeprefix など使えそうな関数があり、これを使ってインデックスを管理せずに書くのもよさそう。

```python

class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()

        sign = 1
        if s.startswith("+"):
            s = s.removeprefix("+")
        elif s.startswith("-"):
            s = s.removeprefix("-")
            sign = -1

        result = 0
        for c in s:
            if not c.isdigit():
                break
            digit = ord(c) - ord("0")
            result *= 10
            result += sign * digit

        result = max(result, -2**31) # compare MIN_INT
        result = min(result, 2**31 - 1) # compare MAX_INT
        return result

```

先頭の一文字だけのチェックだと startswith を使うより s[0] でもいいかもしれない。pep8 で言っているのは、スライスを使う場合のことか。

https://peps.python.org/pep-0008/
> Use ''.startswith() and ''.endswith() instead of string slicing to check for prefixes or suffixes.

```python

sign = 1
if s and s[0] == "+":
    s = s[1:]
elif s and s[0] == "-":
    s = s[1:]
    sign = -1

```

```python

sign = 1
if s and s[0] in "+-":
    if s[0] == "-":
        sign = -1
    s = s[1:]

```

```python

sign = 1
if s.startswith("+"):
    s = s[1:]
elif s.startswith("-"):
    s = s[1:]
    sign = -1

```

## step2

- https://github.com/fhiyo/leetcode/pull/57/files
    - ループの中で、範囲チェックをして return するのもいいかも。
    - ついでに chromium 見てたら以下のようなコードもあった。こういう書き方もするんですね。
        - https://source.chromium.org/chromium/chromium/src/+/main:third_party/opus/src/dnn/torch/lpcnet/utils/pcm.py;l=31?q=lang:python%20INT_MIN
        ```python

        def clip_to_int16(x):
            int_min = -2**15
            int_max = 2**15 - 1
            x_clipped = max(int_min, min(x, int_max))
            return x_clipped

        ```

- https://github.com/olsen-blue/Arai60/pull/60/files
    - index == len(s) になった時点で return 0 するのも自然かもしれない。
    - `num = num * 10 + sign * digit` として、ループの中で return する方法も。

- https://github.com/katsukii/leetcode/pull/9/files
    - python では違うが、overflow を防ぐ目的だと digit を足す前にチェックしないとですね。
        ```java

        if (result > (Integer.MAX_VALUE - digit) / 10) {
            return sign == 1 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
        }


        ```

index を管理しながら各文字をチェックしていく方法。"0123456789" は chromium でも使われていたのが少し意外だった。s.isdigit() や string.digits に比べてドキュメントを見に行かなくてもよさそうなところがいいとこなのかな。s[index] はこの中にあるよっていう感じがして意外と好きかもしれない。（ない場合もあります）

```python

class Solution:
    def myAtoi(self, s: str) -> int:
        index = 0
        while index < len(s) and s[index] == " ":
            index += 1

        sign = 1
        if index < len(s) and s[index] == "+":
            index += 1
        elif index < len(s) and s[index] == "-":
            index += 1
            sign = -1

        MIN_INT = -2**31
        MAX_INT = 2**31 - 1
        result = 0
        while index < len(s) and s[index] in "0123456789":
            digit = ord(s[index]) - ord('0')
            result *= 10
            result += sign * digit
            if result < MIN_INT:
                return MIN_INT
            if result > MAX_INT:
                return MAX_INT
            index += 1

        return result

```

## step3

この形で練習しました。

```python

class Solution:
    def myAtoi(self, s: str) -> int:
        index = 0
        while index < len(s) and s[index] == " ":
            index += 1

        sign = 1
        if index < len(s) and s[index] == "+":
            index += 1
        elif index < len(s) and s[index] == "-":
            index += 1
            sign = -1

        MIN_INT = -2**31
        MAX_INT = 2**31 - 1
        result = 0
        while index < len(s) and s[index] in "0123456789":
            digit = ord(s[index]) - ord("0")
            result *= 10
            result += sign * digit
            if result < MIN_INT:
                return MIN_INT
            if result > MAX_INT:
                return MAX_INT
            index += 1
        
        return result

```