# 283. Move Zeroes

## step1

数値を要素に持つリストが与えられる。すべての0をリストの後ろから後ろに移動させ、0以外をもともとの順番を崩さずに前から詰めていく。
リストの長さは 1 <= nums.length <= 10^4 を想定する。

0ではない要素を見つけたときにそれを挿入できる場所に挿入し、挿入できる場所の情報を正しく更新していくことができればいけそう。
まず、リスト内に0が存在するかどうか調べて、存在しない場合はそこで終了。存在する場合は、0以外の要素を正しい順番で挿入できる場所を常に持っていることを保証する position_to_insert を用意して、リスト内の一番左の0の位置で初期化する。
探索は、start を position_to_insert + 1 の場所で初期化し、そこから開始する。
0を見つけた場合、移動させたい要素がないので何もせずに次のループに進む。0ではない要素を見つけた場合、その要素を position_to_insert が示している場所に置く。このとき、[position_to_insert + 1, i] まですべて0ではない要素を置くことができる場所になっているので、このタイミングで position_to_insert をインクリメントする。ループが終ると、0ではない要素がすべて [0, position_to_insert) の範囲に移動しているので、最後に[position_to_insert, len(nums)) の範囲に0を置けばよさそう。最後に0を置く仕事は、0ではない要素を移動させたときに nums[i] に0を置いておけばなくせるし、0ではない要素を置くことができるという意味で0にしておくのが自然な気がする。

```python

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        if 0 not in nums:
            return 

        position_to_insert = nums.index(0)
        for i in range(position_to_insert + 1, len(nums)):
            if nums[i] == 0:
                continue

            nums[position_to_insert] = nums[i]
            position_to_insert += 1
            nums[i] = 0

```

時間計算量: O(n)
- Python で1秒間に100万ステップ処理できるとすると、だいたい0.01秒くらいでみておく。
空間計算量: O(1)

sequence.index: https://docs.python.org/3/library/stdtypes.html#sequence.index
- 要素が存在しない場合は ValueError を返す。

空のリストが与えられたとき、現状 `if 0 not in nums:` の中に入る。これは、動かすものがなかったという意味でそのままでいいと思う。
position_to_insert は短くできないか考える。
他の方法は思いつかなかった。

## step2

- https://github.com/fhiyo/leetcode/pull/54/files
    - 途中でリストを使ってはいけないわけではないですね。。勝手な思い込みをしていました。シンプルでわかりやすい。
    - 例外について: https://github.com/fhiyo/leetcode/pull/54/files#r2021355464
    - [:last_nonzero_index] の要素がすべて0ではない範囲の last_non_zero_index を使うという考えもある。nonzero の要素を再度置きなおすという発想が自分にはなかったからこの考えにならなかったのかな。変数名はちょっと変えたい気もする。
    - 0を入れるのではなく、スワップさせるのもいいか。 

- https://github.com/olsen-blue/Arai60/pull/55/files
    - nonzero な要素をすべて移動させてループを終了したあと後ろに0を置いていく方が分かりやすい気がしてきたかも。

- https://github.com/SuperHotDogCat/coding-interview/pull/25/files
    - step1 で min 関数を使っているところが分かりにくかったかも。実質ループの中で一回しか使われてない気がするので外に出したりしたいな。

- https://github.com/Yoshiki-Iwasa/Arai60/pull/59/files
    - こういうのがあるらしい
        - https://en.wikipedia.org/wiki/Erase%E2%80%93remove_idiom
            - c++ で、 vector のようなコンテナで erase を複数回呼ぶときの、大きな移動コストを何とかしたい、というのがモチベーションみたい。
        - https://en.cppreference.com/w/cpp/algorithm/remove.html
            - find してる方もいい。
            - これは、移動元には何もしていないっぽい。

- https://discord.com/channels/1084280443945353267/1210494002277908491/1211368894669787226
    - cpp のコードになるが参考に見ておく。
    
これもいいですね。

```python

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        nonzeros = [num for num in nums if num != 0]
        for i, nonzero in enumerate(nonzeros):
            nums[i] = nonzero
        for i in range(len(nonzeros), len(nums)):
            nums[i] = 0

```

non zero の要素の数を数えていき、[:non_zero_count) の範囲に0が含まれないようにする。0の処理は一つ目のループを出た後にした方が分かりやすいかな。
最初の0を見つけるまでは、non_zero_count == i のときにも nums[non_zero_count] = nums[i] が実行されているのが気になるような気もするし考えすぎな気もする。

```python

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        non_zero_count = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                continue
            nums[non_zero_count] = nums[i]
            non_zero_count += 1

        for i in range(non_zero_count, len(nums)):
            nums[i] = 0

```

step1 で position_to_insert という変数名を使ったが、insert にするとずらすニュアンスが出るかもしれないので、destination_index の方がいいかな。

```python

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        if 0 not in nums:
            return 

        destination_index = nums.index(0)
        for i in range(destination_index + 1, len(nums)):
            if nums[i] == 0:
                continue
            nums[destination_index] = nums[i]
            destination_index += 1

        zero_fill_start = destination_index
        for i in range(zero_fill_start, len(nums)):
            nums[i] = 0

```

## step3

この形で練習しました。

```python

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        non_zero_count = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                continue
            nums[non_zero_count] = nums[i]
            non_zero_count += 1

        for i in range(non_zero_count, len(nums)):
            nums[i] = 0

```