# 1011. Capacity To Ship Packages Within D Days

## step1 

capacity に制約はないのでどんな積載容量を持った船でも用意できるとすると、D 日以内で運べない場合は考えなくてもいいのか。1日ですべて運んでくださいと言われた時を最大とすると、船の積載容量は 1 <= capacity <= 500 * 5 * 10^4 で、上限をだいたい10^7で考えてよさそう。
二分探索で、D 日で運ぶことができる積載容量の最小値を探す。これを実現するために、ある積載容量の船を使って D 日以内で運べるかどうかがわかるといいか。

見つけたいもの target を以下のように設定する。
    - target: D 日以内で運べるという条件を満たす船の積載容量の最小値
left と right の不変条件を以下のように設定する。
    - left: この位置より左に target が存在しない
    - right: この位置より右に target が存在しない
今回は [left, right] に必ず target が存在していて、middle は left <= middle <= right の制約があるとする。
middle の位置によって、left と right を以下のように更新する。
    - middle が target の位置より左側にある場合: [left, middle] に target はないので、left = middle + 1 で更新する
    - middle が target の位置もしくは target の位置より右側にある場合: [middle + 1, right] に target はないので right = middle で更新する
left == right になったときにループを停止させると、left より左に target が存在せず、left より右に target が存在しない位置に left があり、ここが target の位置になる。

問題異なりますが、停止性について以下の議論を参考に理解をしており、今回の middle の制約と left と right の更新方法をから、middle の制約を満たす選び方をし続ければ left == right になると思っています。実装については、left == right で停止するので、(left + right) // 2 の計算方法で middle の制約を満たす選び方ができていると考えています。
何か足りないところなどあればご教授いただけますと幸いです。

https://discord.com/channels/1084280443945353267/1192736784354918470/1199018938005213234
>  middle の選び方は、left <= middle <= right であれば、この議論だとどこでも大丈夫なはずです。区間は、最低1減っていきますから。

```python

class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def can_ship_within_days(capacity: int) -> bool:
            load = 0
            required_days = 1
            for weight in weights:
                if capacity < weight:
                    return False
                if load + weight <= capacity:
                    load += weight
                    continue
                required_days += 1
                load = weight
            return required_days <= days

        left = 1
        right = sum(weights)
        while left < right:
            middle = (left + right) // 2
            if can_ship_within_days(middle):
                right = middle
            else:
                left = middle + 1
        return left

```

## step2

- https://github.com/SuperHotDogCat/coding-interview/pull/27/files
    - step3 で、ある capacity で運べるか調べるとき、capacity を超えたときを if 文の中に入れる書き方わかりやすいです。
    - capacity の最小を 1 で考えたけど、実際は weights の最小値になりますね。

https://github.com/saagchicken/coding_practice/pull/10/files
    - ある capacity で運べるか調べるとき、載せられる場所の残りで考えることもできますね。
    - left や right は変数名変えた方がいいのかどうか。もう少し考えよう。

- https://github.com/sakupan102/arai60-practice/pull/45/files
    - days = 0 が来たときを考えてなかった。
    - days = 0 で required_days >= 1 なので、can_ship_within_days が必ず False を返す。よって、left + 1 が続き、必ず right の初期値 sum(weights) で止まる。悩むけど ValueError を投げよう。
        - 参考: https://github.com/python/cpython/blob/60732d7397485262bd9fec4b017d029dd16b5e3a/Lib/bisect.py#L74
    - weights が空の場合は max でエラーになり、それでいい気がする。

- https://github.com/fhiyo/leetcode/pull/45/files
    - range 関数を使う方法もあると。

```python

class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        if days < 1:
            Raise ValueError('days must be greater than 0')

        def can_ship_within_days(capacity: int) -> bool:
            load = 0
            required_days = 1
            for weight in weights:
                if capacity < weight:
                    return False
                if capacity < load + weight:
                    load = 0
                    required_days += 1
                load += weight
            return required_days <= days

        left = max(weights)
        right = sum(weights)
        while left < right:
            middle = (left + right) // 2
            if can_ship_within_days(middle):
                right = middle
            else:
                left = middle + 1
        return left

```

left を変更したので if capacity < weight は必要なくなったけど、can_ship_within_days 関数だけを見ていると weight だけをのせる場合のチェックがないことに驚くかもしれないので残してもいい気はする。
right = sum(weights) + 1 にはしないほうが自然な気がする。

## step3

この形で練習しました。
二分探索だけではないと思いますが、書き方の話をするときは、まず何をしたいのかを決めてから行うことが大事だと感じました。

```python

class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        if days <= 0:
            raise ValueError('days must be greater than 0')
        
        def can_ship_within_days(capacity: int) -> bool:
            required_days = 1
            load = 0
            for weight in weights:
                if capacity < weight:
                    return False
                if capacity < load + weight:
                    load = 0
                    required_days += 1
                load += weight
            return required_days <= days

        left = max(weights)
        right = sum(weights)
        while left < right:
            middle = (left + right) // 2
            if can_ship_within_days(middle):
                right = middle
            else:
                left = middle + 1
        return left

```
