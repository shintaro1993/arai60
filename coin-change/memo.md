# 322. Coin Change

## step1

コインと金額が与えられるので、その金額にするために使うコインの最小の枚数を求める。（それぞれの種類のコインは何枚でも使ってよい）

考えたこと:
- どのコインを使ったかを覚えておく必要はない
- 部分問題を解決した後に元の問題に取り組むとよさそう。mount が0の場合から順に解決していく。
- ある金額について、coins[i] を使った場合の最小枚数を計算していく。
- コインの枚数は (1 <= coins.length <= 12) でこれを n として、金額は（0 <= amount <= 10^4）でこれを m とすると、時間計算量は O(nm) で上限を入れて計算すると0.12秒くらいかかりそう

```python

import math


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        min_num_coins = [math.inf] * (amount + 1)
        min_num_coins[0] = 0
        for sub_amount in range(1, amount + 1):
            for coin in coins:
                if sub_amount - coin < 0:
                    continue
                if math.isinf(min_num_coins[sub_amount - coin]):
                    continue
                min_num_coins[sub_amount] = min(
                    min_num_coins[sub_amount], min_num_coins[sub_amount - coin] + 1
                )

        if math.isinf(min_num_coins[amount]):
            return -1
        return min_num_coins[amount]

```

ループを、sub_amount ではなく amount で回したかった。target とかもいいかな。
`sub_amount - coin` は3回出てきているので変数においてもいいかも。いい感じのが思いつかないけど complement とかかな。

isinf: https://docs.python.org/3/library/math.html#math.isinf

## step2

- https://github.com/sakupan102/arai60-practice/pull/41/files
    - current_amount と prev_amount や sum_coin などあった。もう一度考えてみよう。
    - 私も step1 よりは、step2 で early return している方が読みやすいと思う。
    - 個人的には `return num_fewest_coins[-1]` の -1 を amount にした方が分かりやすいかな。

- https://github.com/fhiyo/leetcode/pull/41/files#r1679585050
    - ループの中で新しい金額を計算して、その枚数を更新していく方法もある。これは好みなのかな。
    - dp のリストを -1 で初期化して、ループの先頭で `if num_coins_list[i] == -1` なら continue していて、これはもう少し下まで読まないと理由が分からないと感じる。
    - トップダウンの方法や、最短経路問題として考えることもできる。

- https://github.com/olsen-blue/Arai60/pull/40/files
    - BFS のコードが分かりやすく書かれていた。
    - 各コインの金額を足したノードたちを下にはやしていくイメージで理解した。

- https://github.com/Fuminiton/LeetCode/pull/40
    - セルフレジなど現実の状況を考えているのは大事ですね。
    - 金額を作れなかった場合が -1 なので、amount が None などの場合は ValueError にしたい気持ちかもしれない。よく考えると難しい。
    - min 関数内の引数は、このくらいの長さになると縦に並べた方が読みやすいと感じた。

BFS で探索して、見つけたところで return する方法。

```python

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0
        
        coin_sums = [0]
        seen = set([0])
        num_coins = 1
        while coin_sums:
            next_coin_sums = []
            for coin_sum in coin_sums:
                for coin in coins:
                    next_coin_sum = coin_sum + coin
                    if next_coin_sum == amount:
                        return num_coins
                    if next_coin_sum > amount:
                        continue
                    if next_coin_sum in seen:
                        continue
                    next_coin_sums.append(next_coin_sum)
                    seen.add(next_coin_sum)
            num_coins += 1
            coin_sums = next_coin_sums
        return -1

```

DFS よりはこちらの方が合っていると思う。
変数名は、できるだけ自分の中でしっくりくるものを探しつつ、他の人と議論していくのがよさそうだと思った。
シンプルに実装できそうと思ったが結構ネストが深くなっているなと感じた。二重ループの中を関数に切り出すのもいいかと思ったが、next_coin_sum が amount になった場合のことを考えるとなかなかいい案が思い浮かばない。`for coin in coins` 自体を関数に切り出せればすっきりしそうだけど難しい。

```python

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0
        
        def maybe_append(next_coin_sums: List[int], seen: Set[int], coin_sum: int) -> None:
            for coin in coins:
                next_coin_sum = coin_sum + coin
                if next_coin_sum > amount:
                    continue
                if next_coin_sum in seen:
                    continue
                next_coin_sums.append(next_coin_sum)
                seen.add(next_coin_sum)
            
        coin_sums = [0]
        seen = set([0])
        num_coins = 0
        while coin_sums:
            next_coin_sums = []
            for coin_sum in coin_sums:
                if coin_sum == amount:
                    return num_coins
                maybe_append(next_coin_sums, seen, coin_sum)
            num_coins += 1
            coin_sums = next_coin_sums
        return -1

```

関数名は `maybe_append_next_coin_sum` の方がわかりやすいかどうか。

トップダウンの方法

```python

import math
import functools


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        @functools.cache
        def get_min_num_coins(coin_sum: int) -> int:
            if coin_sum == 0:
                return 0
            min_num_coins = math.inf
            for coin in coins:
                remaining_sum = coin_sum - coin
                if remaining_sum < 0:
                    continue
                num_coins = get_min_num_coins(remaining_sum) + 1
                min_num_coins = min(min_num_coins, num_coins)
            return min_num_coins    

        min_num_coins = get_min_num_coins(amount)
        if math.isinf(min_num_coins):
            return -1
        return min_num_coins

```

step1 の改善
BFS やトップダウンよりはこちらが分かりやすいと思う。

```python

import math


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        min_num_coins = [math.inf] * (amount + 1)
        min_num_coins[0] = 0
        for target in range(1, amount + 1):
            for coin in coins:
                remaining_amount = target - coin
                if remaining_amount < 0:
                    continue
                if math.isinf(min_num_coins[remaining_amount]):
                    continue
                min_num_coins[target] = min(
                    min_num_coins[target], 
                    min_num_coins[remaining_amount] + 1
                )

        if math.isinf(min_num_coins[amount]):
            return -1
        return min_num_coins[amount]

```

## step3

step2 と同じですがこちらで練習しました。
`min_num_coins` は `amount_to_min_num_coins` の方が意図にあっていると思いましたが、短い方が読みやすいかと思いそのままにしました。

```python

import math


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        min_num_coins = [math.inf] * (amount + 1)
        min_num_coins[0] = 0
        for target in range(1, amount + 1):
            for coin in coins:
                remaining_amount = target - coin
                if remaining_amount < 0:
                    continue
                if math.isinf(min_num_coins[remaining_amount]):
                    continue
                min_num_coins[target] = min(
                    min_num_coins[target],
                    min_num_coins[remaining_amount] + 1
                )
        
        if math.isinf(min_num_coins[amount]):
            return -1
        return min_num_coins[amount]

```

