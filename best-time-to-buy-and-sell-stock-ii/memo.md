# 122. Best Time to Buy and Sell Stock II

## step1

株を売りたい気持ちになるのは値段が一番高くなったところだと思う。値段が下がった後も売らずに最高値を更新するのを待った方がいいかというと、値段が下がる直前で持っている株を売って、下がったところで再度買っていく方が利益を高くすることができる。
例えば、prices = [1, 3, 2, 4] のとき、
1. 1で買って4で売ると利益は3
2. 1で買って3で売って、2で買って4で売ると利益は4
になるので、この考え方でよさそう。

作業の内容としては、現在の利益と直近における最小値と最大値を管理してループを回していく。ループの先頭で、prices[i] が直近における最大値より大きければ値を更新して次のループへいく。prices[i] の方が小さければ、直近における最大値と最小値の和をとって現在の利益に加える。その後、最小値と最大値を prices[i] に更新して次のループに行くという感じで実装をしてみる。

```python

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        if len(prices) == 1:
            return 0

        result = 0
        max_price = prices[0]
        min_price = prices[0]
        for i in range(1, len(prices)):
            if prices[i] > max_price:
                max_price = prices[i]
                continue
            result += max(max_price - min_price, 0)
            max_price = prices[i]
            min_price = prices[i]
        result += max(max_price - min_price, 0)
        return result

```

最高値を更新できないときに現在の利益を確定させているので、最高値を更新中でループが終った場合、ループの外で後始末をしないといけないのが気になる。

## step2

- https://github.com/fhiyo/leetcode/pull/39/files
    > 当日と前日を比べて当日の方が高くなっていたら、前日に買ったことにしてその場で売る、を繰り返せばよい。
    - この考えの方が自然かもしれない。実装もシンプルになる。

- https://github.com/olsen-blue/Arai60/pull/38/files
    > yesterday_price は prices[i - 1] でも大丈夫そうかな。変数に置かない方が好みかも。
    - max_profit に違和感があって result にしていたけど、「現在までの」という意味で考えると大丈夫そうだ。   

- https://github.com/Fuminiton/LeetCode/pull/38/files
    - 自分と同じで、`if len(prices) == 1:` を書かれていている。自分も書きたい。感覚としては、「あってもいいですが、これはなくてもいいですね。」くらいらしい。

- https://github.com/Mike0121/LeetCode/pull/53/files
    - 動的計画法はちょっと読むの難しい。hold で `not_hold[day - 1] - price` しているのは、買うことでお金を払ったということなのか。

remove duplicate from sorted list のときのように、一つの作業のまとまりが大きすぎてループの外に仕事が残ってしまう、ということを今回もやった気がするのでもう少し小さく考えていこうと思う。

自然かなと思うのは以下の二つで、比べてみると、上の方は i と i - 1 を二か所ずつ書いていて、書き間違いするかもしれないことを考えると下の方がいいのかも。

```python

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                max_profit += prices[i] - prices[i - 1]
        return max_profit

```

```python

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        for i in range(1, len(prices)):
            max_profit += max(prices[i] - prices[i - 1], 0)
        return max_profit

```

## step3

i を day などにした方がいいか迷いましたが、今回は普段見慣れている i の方が読みやすいかと思いそのままにしました。
また、このくらいのコード量だと early return はしなくてもいいかと思いました。

```python

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        for i in range(1, len(prices)):
            max_profit += max(prices[i] - prices[i - 1], 0)
        return max_profit

```