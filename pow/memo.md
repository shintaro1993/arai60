# 50. Pow(x, n)

## step1

x と n を受け取って x^n を返す。x = 0 かつ n <= 0 の場合は不正な入力として処理する。
例えば、2^5 = 2 * 2 * 2 * 2 * 2 のように n 回ループを回すと行けそう。
ただし、-2^31 <= n <= 2^31-1 であること、Python で1秒間に100万ステップ処理できることを仮定して、単純に n 回ループを回すと 2,147,483,647 / 1,000,000 となり、おおよそ35分くらいかかりそうかな。

pow(x, n) = pow(x, n/2) * pow(x, n/2) で計算できる。n が奇数のときは追加で x をかけるといけそう。

```python

class Solution:
    def pow_helper(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0
        if n == 1:
            return x
        half_pow = self.pow_helper(x, n // 2)
        result = half_pow * half_pow
        if n % 2 == 1:
            result *= x
        return result

    def myPow(self, x: float, n: int) -> float:
        if x == 0.0 and n <= 0:
            raise ValueError("invalid input")

        if n < 0:
            x = 1.0 / x
            n = abs(n)
        return self.pow_helper(x, n)

```

Numeric Types — int, float, complex: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
class float: https://docs.python.org/3/library/functions.html#float
pow: https://docs.python.org/3/library/functions.html#pow
cpython pow: https://github.com/python/cpython/blob/4641925bf27d9ca09b88e3063a391931da3e7c0c/Objects/longobject.c#L4983
    - ValueError を出そうと思っていたが、pow 関数が "ZeroDivisionError: 0.0 cannot be raised to a negative power" を出していることに気づいた。
    - 0^-1 = 1/0 で ZeroDivisionError ですかね。ただし pow は x = 0 n = 1 で 1 を返している。問題の制約でこれものぞこう。
    - 以下では、0^0 = 1 と書かれている
        - https://en.wikipedia.org/wiki/Zero_to_the_power_of_zero?utm_source=chatgpt.com
        > All three of these specialize to give 0^0 = 1.

math.pow: https://docs.python.org/3/library/math.html#math.pow
cpython math.pow: https://github.com/python/cpython/blob/d4e5802588db3459f04d4b8013cc571a8988e203/Modules/mathmodule.c#L3050
    - 入力に NaN が含まれる場合も想定している。
    - NaNs: https://en.wikipedia.org/wiki/IEEE_754

例外処理などを修正する

```python

class Solution:
    def _pow_helper(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0
        half_pow = self._pow_helper(x, n // 2)
        result = half_pow * half_pow
        if n % 2 == 1:
            result *= x
        return result

    def myPow(self, x: float, n: int) -> float:
        if x == 0.0 and n == 0:
            raise ValueError("Either x must be non-zero or n must be greater than 0")
        if x == 0.0 and n <= 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")

        if n < 0:
            x = 1.0 / x
            n = abs(n)
        return self._pow_helper(x, n)

```

## step2

- https://github.com/Fuminiton/LeetCode/pull/45/files
    - 関数の引数は base, exp の方が読みやすいかな。ライブラリの pow とそろえているし。
    - 関数名は helper じゃなくて、calculate_pow の方が読みやすいかも。
    - この資料も: https://docs.python.org/3/tutorial/floatingpoint.html

- https://github.com/hroc135/leetcode/pull/43/files
    - 再帰をループになおすことができていないので考える
    - そもそも、positivePow(x*x, quotient) としているので、自分とは違う形の再帰ですかね。
        (2^1)^10 	=	(2^2)^5
        (2^2)^5		=	(2^4)^2 * (2^2)
        (2^4)^2		=	(2^8)^1
        (2^8)^1		=	(2^16)^0 * (2^8)
        (2^16)^0	=	1
        これをコードにしているということかな。まだ頭の中が整理できていない気がする。
    - bit 利用するのは思いつきませんでした。
    - 例外処理については、改めて cpython などを見ながら整理しよう。

- https://github.com/Ryotaro25/leetcode_first60/pull/48/files
    - float の内部実装も見ておく

- https://github.com/Yoshiki-Iwasa/Arai60/pull/38/files
    - 再帰関数の呼び出しが終った後に 1.0 / powerd するかどうか調べるのもいいかも。
    - n = abs(n) としなくても、(x, abs(n)) でもいいかもしれない。

hroc135 さんの PR を見て考えたことをもとに書いてみる。

```python

class Solution:
    def _calculate_pow(self, base: float, exponent: int) -> float:
        if exponent == 0:
            return 1.0
        result = self._calculate_pow(base * base, exponent // 2)
        if exponent % 2 == 1:
            result *= base
        return result

    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x = 1.0 / x
        return self._calculate_pow(x, abs(n))

```

これなら自然な感じでループにできそう。

```python

class Solution:
    def myPow(self, x: float, n: int) -> float:
        result = 1.0
        base = x
        if n < 0:
            base = 1.0 / x
        exponent = abs(n)
        while exponent > 0:
            if exponent % 2 == 1:
                result *= base
            base *= base
            exponent //= 2
        return result

```

## step3

この形で練習しました。base と exponent の初期化は悩みました。x と n をまた使いたくなった時のことを考えたりしました。exponent を if n < 0 の外側で abs(n) とするのは意外と忘れてしまうなと感じたので if 文の中でまとめて処理しました。
float や IEEE754 周辺はよくわかっていないとこなので、この機会に整理していこうと思いました。

```python

class Solution:
    def myPow(self, x: float, n: int) -> float:
        result = 1.0
        base = x
        exponent = n
        if n < 0:
            base = 1.0 / x
            exponent = -n
        while exponent > 0:
            if exponent % 2 == 1:
                result *= base
            base *= base
            exponent //= 2
        return result

```
