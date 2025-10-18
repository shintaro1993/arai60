# 779. K-th Symbol in Grammar

## step1

複数の行があり、行には複数のシンボルがある。1行目にシンボルとして0が1つあるところから始める。左のシンボルから調べていき、0の場合0と1を、1の場合1と0を次の行の左端から詰めて置いていく。これを繰り返し、n 行目の k 番目にあるシンボルを返す。

最初は各行のシンボルをリストとして持ち、幅優先探索のようにリストを更新していき、最後のリストの k 番目を返すとよさそうかなと思った。下のようなコードを考えました。

```python

class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        symbols = [0]
        for _ in range(n - 1):
            next_symbols = []
            for symbol in symbols:
                if symbol == 0:
                    next_symbols.append(0)
                    next_symbols.append(1)
                else:
                    next_symbols.append(1)
                    next_symbols.append(0)
            symbols = next_symbols
        return symbols[k - 1]

```

extend() の方がよさそうか。https://docs.python.org/3/library/stdtypes.html#list.extend
どちらにせよ、これだと時間計算量がO(2^n)、空間計算量がO(2^n)で、n = 30 を考えると途中からリストがメモリにのらなくなりそうですし、他の方法も考えたいと思う。

ある行における symbol をすべて持っておく必要はなく、1行目の1つ目の symbol を更新しながら n 行目の k 個目の symbol まで下りていくことができればよさそう。下っていくときの各根において、中央の symbol のインデックス（二つある）がわかれば、k がそれ以下か、より大きいかで下りる方向を判断できそう。

```python

class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if n <= 0 or k <= 0:
            raise ValueError("n and k must be greater than 0")

        symbol = 0
        nums_leaf = 2 ** (n - 1)
        middle_index = nums_leaf // 2
        for _ in range(n - 1):
            if k <= middle_index:
                nums_leaf //= 2
                middle_index -= nums_leaf // 2
            else:
                symbol ^= 1
                nums_leaf //= 2
                middle_index += nums_leaf // 2
        return symbol

```

木を考えているときに index という変数名を使わないほうがよさそうかな。

## step2

- https://github.com/tokuhirat/LeetCode/pull/46/
    - f(n, k) で開始して、行くときに n = 1 までの n と k の組を確定させ、戻るときにシンボルを更新していく方法もありますね。わかりやすいです。（コードは0インデックスにされています。）
    - 葉から根まで登りながら更新していく気持ちがなかったですが、言われてみるとわかりやすいかもしれない。

- https://github.com/TORUS0818/leetcode/pull/48
    - k や symbol の更新の仕方はいろいろありますね。ビット演算じゃない方が好きかも。

- https://github.com/olsen-blue/Arai60/pull/47
    > kの値にどう結びつくのかイメージできずでしたが、k-1 の二進数表記はルートからの移動パターンなんですね。
    - 考えもしませんでした。
        - https://docs.python.org/3/library/stdtypes.html#int.bit_count

葉から根まで登りながら symbol を反転させていく方法が分かりやすく感じました。
step1 で下りるときの逆だと思いますが、ある行において偶数番目のシンボルから上に上るときに反転がおきるので処理をします。

```python

class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if n <= 0:
            raise ValueError("n must be greater than 0")
        if k < 1 or 2 ** (n - 1) < k:
            raise ValueError("k must be between 1 and 2 ** (n - 1)")

        result = 0
        while k > 1:
            if k % 2 == 0:
                result = 1 - result
            k = (k + 1) // 2
        return symbol

```

## step3

私の気持ちとしては、n 行目 の k 番目から上に登りながら symbol を更新していくというものでしたが、開始地点の symbol はわかっていないはずなので0で初期化することに少し違和感があり、反転させた数を数える、に変えました。どう考えるのがいいかはもう少し考えようと思います。

```python

class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if n <= 0:
            raise ValueError("n must be greater than 0")
        if not 1 <= k <= 2 ** (n - 1):
            raise ValueError("k must be between 1 and 2 ** (n - 1)")
        
        flip_count = 0
        while k > 1:
            if k % 2 == 0:
                flip_count += 1
            k = (k + 1) // 2
        return flip_count % 2

```
