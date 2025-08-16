# 300. Longest Increasing Subsequence

## step1

### approach a

すべての部分列を作り、増加部分列である部分列の長さの中で最大の長さを返します。(./step1/approach_a_1.py)
そこから、条件を満たしていないことが分かった段階で探索を打ち切るように変形させました。(./step1/approach_a_2.py)
時間計算量は O(2^n) で、部分列を作る作業において重複している部分があるので何とかしたいという気持ちが生まれる。

### approach b

nums の i 番目の要素を末尾に持つ増加部分列の長さに注目します。この長さは、0 <= j <= i-1 の範囲で nums[j] < nums[i] を満たす要素を探し、その nums[j] を末尾とする増加部分列の長さ + 1 の中から最大値を取ることで求められると思います。
この考え方をもとに実装します。(./step1/approach_b.py)  

二重ループで使っている i と j という変数名を説明的にした方がいいかなと感じたがよいものが思い浮かばない。
外側の for ループのインデックスが1から始まるのは少し気になるかもしれない。

## step2

### 調べたこと・読んだコード

- https://github.com/Mike0121/LeetCode/pull/50/files
    - 長さ l の増加部分列の末尾の最小値を更新していくことで、最大の増加部分列の長さを求めるというものがある。最小値の更新を二分探索で行うことで計算量を O(nlogn) にしている。
    - 個人的には、二分探索をする前に、リストが空の場合もしくはリストの末尾の値より大きい場合に新しい要素をリストの末尾に追加する方が分かりやすい気がするかも。

- https://discord.com/channels/1084280443945353267/1200089668901937312/1209534429593210932
    - 動的計画法を使ったコードの、二重ループのインデックスの部分はよい変数名を付けるのが難しいですね。関数化して処理の意図を伝えようとするのはこれからも意識しておこうと思う。

- https://github.com/shining-ai/leetcode/pull/31
    - やっぱり二重ループで i と j を使うのであればコメントを残した方がよさそう。

- https://github.com/ryosuketc/leetcode_arai60/pull/44
    - ネストの深さにも気をつけよう。

step1 の approach_b.py を修正しました。(./step2/approach_b_2.py)
変数名は長くなるけど、i と j でループを回すよりはいいと思う。

二分探索を使って書きました。(./step2/approach_c_1.py)

https://docs.python.org/3/library/bisect.html
https://github.com/python/cpython/blob/8d6e1075dac0fd04211c8159f0599b243cb1c4b0/Lib/bisect.py#L21

二分探索を行う前に、リストの末尾に追加する場合を処理して continue させようと思いましたがわかりにくくなってしまったので、(./step2/approach_c_2.py)で修正しました。

## step3

index_to_insert -> insert_position に変更して練習しました。(./step3/approach_c_3.py)

