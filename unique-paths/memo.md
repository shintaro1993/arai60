# 62. Unique Paths

## step1

スタート地点からゴール地点までの異なる経路の数を求める。
スタート地点からある地点までの経路の数は、ある地点の一つ上と左の地点までの経路の数の和になる。二次元のリスト path_counts[m][n] でスタート地点からここまでの経路の数を表現してこれを埋めていけば大丈夫そう。(step1/approach_a.py)

時間計算量は O(m*n) で、m と n をそれぞれ100と仮定すると、見積もった結果は0.01秒くらいで、計測結果は0.002254だった。
空間計算量は O(m*n) 

## step2

### 読んだコード

- https://github.com/saagchicken/coding_practice/pull/19/files
    - 二次元配列の初期化を `dp_paths[0][0] = 1` とするのも意外とすっきりしているかもしれない。

- https://github.com/nittoco/leetcode/pull/26/files
    - comb モジュールも読んでみよう。

- https://github.com/sakupan102/arai60-practice/pull/34/files
    - 再帰で書く方法もあるんですね。
    - 二次元配列を1で初期化するとコードは短くなるけど、好みではないかな。
    - おお、`return ways[-1][-1]` の方が読みやすいかもしれない。

- https://github.com/fhiyo/leetcode/pull/34/files
    - num_paths の方がわかりやすいか。
    - 空間計算量 O(m) または O(n) の方法もあるんですね。どうすれば思いついただろうか。

step1 のコードの書き方を変えてみる。(step2/approach_b.py)
変数名は変えた方がよくなった気がする。個人的にはループの外で準備をしておきたい気持ちかな。

空間計算量を改善した方法。(step2/approach_c.py)
この書き方だと、リストを1で初期化してループを1から始めるのが自然だと感じる。

comb のコードを読んでみる
- https://docs.python.org/3/library/math.html#math.comb
- https://github.com/python/cpython/blob/eae9d7de1c45a64076a926d53672823e6ae1777d/Modules/mathmodule.c#L3904

気になることができたときに読むとさらに良いのかもしれない。

## step3

step3/approach_d.py で書く練習を行いました。
二重ループの外で num_paths の一部を1で埋める処理をするとき、最初インデックスは i でもいいかなと思ったが、それぞれを row と column にした方が何がどこを走っているのか、どっちに0を指定すればいいのかがつながって感じられたので i ではない方がよいと感じた。
