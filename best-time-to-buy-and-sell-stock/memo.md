# 121. Best Time to Buy and Sell Stock

## step1

i 日目の金額で売ることを考えたとき、0から i-1 日目のどこで買うのがいいかを調べていけば、O(n^2) で計算することができる。買いたい日は0から i-1 日の中の一番安い日なので、すべてを調べなくても過去の最小値を持っていれば i 日目で売る場合の最大の金額がすぐに計算できる。
今回の問題では買う人売る日は別の日にしないといけないので、リストのサイズが1の場合は0を返す。ループはリストの2番目から回していくのが自然かな。そうすると過去の最小値はリストの一番目でいいかな。問題文を読んだ限り利益がない場合は0を返すようにとのこと。リストが空の場合も、最大の利益が存在しないという意味で0を返すということにしておこう。

```python

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        if len(prices) == 1:
            return 0
        
        max_profit = 0
        min_price = prices[0]
        for i in range(1, len(prices)):
            max_profit = max(max_profit, prices[i] - min_price)
            min_price = min(min_price, prices[i])
        return max_profit

```

今回は prices の値に負の値は来ないことを想定しているけれども、この実装では負の値が来た場合も動いてしまう。動いても大丈夫か。
`if len(prices) == 1` の部分はなくても動くか。ループも prices の先頭から始めても動くか。ただ先頭の金額で売ることはできないのでそれは違和感があるかも。

## step2

https://github.com/kzhra/Grind41/pull/4/files
	- 買う日を固定して、売る日を探していく考え方も。

https://github.com/Fuminiton/LeetCode/pull/37/files
	- for price in prices[1:] で回すのはありかも。

https://github.com/hayashi-ay/leetcode/pull/52/files
	- max_profit = 0 の次にmin_price_so_far = prices[0] を持ってきたいと思った。

prices の先頭からループを回す方法も書いてみます。

```python

import math


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        min_price = math.inf
        for price in prices:
            max_profit = max(max_profit, price - min_price)
            min_price = min(min_price, price)
        return max_profit

```

1回目のループで、price - math.inf をしているのが少し気になるかも。
min_price の初期値は、price[0] で profit が0以下になればいいので prices[0] をセットすることもできるが個人的にはあまり好みじゃないかも。

## step3

step1 と同じになってしまいましたが以下のコードで練習しました。

```python

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        if len(prices) == 1:
            return 0
        
        max_profit = 0
        min_price = prices[0]
        for i in range(1, len(prices)):
            max_profit = max(max_profit, prices[i] - min_price)
            min_price = min(min_price, prices[i])
        return max_profit

```
