# 49. Group Anagrams

## Step1

- リストに含まれる文字列を、アナグラムごとに分けて返す

- 辞書を使ってアナグラムを管理します。ソートした単語をキーとして、それに対するアナグラムたちをそのキーに対するリストに追加していきます。

- 辞書のキーは hashable である必要がありますが、sorted が list を返すので、hashable にする必要があります。
    - https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
        > A mapping object maps hashable values to arbitrary objects. 
    - https://docs.python.org/3/library/functions.html#sorted
        > Return a new sorted list from the items in iterable.
    - https://docs.python.org/3/library/stdtypes.html#str.join
- hashasbleについて
    - tuple と frozensets は、要素が hashable の場合だけ hashable として扱われる。
        - https://docs.python.org/3/glossary.html#term-hashable
            >  Most of Python’s immutable built-in objects are hashable; mutable containers (such as lists or dictionaries) are not; immutable containers (such as tuples and frozensets) are only hashable if their elements are hashable.
- ファイルに書き込む要領で文字列を結合するものも紹介されていました。
    - https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
        > There is also no mutable string type, but str.join() or io.StringIO can be used to efficiently construct strings from multiple fragments.

- 見積り
    - リストの大きさ: n
    - 文字列の長さ: m
    - 時間計算量：O(n * mlogm)
    - 空間計算量：O(n*m)

```python

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_word_to_anagrams = {}
        for word in strs:
            sorted_word = "".join(sorted(word))
            if sorted_word not in sorted_word_to_anagrams:
                sorted_word_to_anagrams[sorted_word] = []
            sorted_word_to_anagrams[sorted_word].append(word)
        return [anagrams for anagrams in sorted_word_to_anagrams.values()]

```

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_word_to_anagrams = {}
        for word in strs:
            sorted_word = tuple(sorted(word))
            if sorted_word not in sorted_word_to_anagrams:
                sorted_word_to_anagrams[sorted_word] = []
            sorted_word_to_anagrams[sorted_word].append(word)
        return [anagrams for anagrams in sorted_word_to_anagrams.values()]
```

```python

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_word_to_anagrams = defaultdict(list)
        for word in strs:
            sorted_word = tuple(sorted(word))
            sorted_word_to_anagrams[sorted_word].append(word)
        return [anagrams for anagrams in sorted_word_to_anagrams.values()]

```

- 入力のチェックをするにしても、tuple の場合は hashable ではない場合もあるとのことで、読んでいる人にその可能性を意識させないためにも、辞書のキーとして使う場合は、join を使った方がよいかと思いました。

- 入力は `lowercase English letters` とのことです。アナグラムのグループを取得することが目的だと感じたので、英小文字以外の文字を見つけた場合は、その単語だけをはじくだけでよさそうかなと思います。小文字でという要件なので、大文字を小文字に変換するのは違う気がしました。ただ、パラメータで切り替えられるようにするのはありかもしれないと思いました。
- もし空のリストが与えられてしまった場合は、[] か None を返すのが個人的な選択肢ですが、現状の [] でいいかなと思いました。
- 全体としてどういう振る舞いが好ましいのか、他の方のコードを参考にさせていただきながら考えてみようと思います。

- isalpha や islower 関数は日本語を通してしまうんですね。
    - https://docs.python.org/3/library/stdtypes.html#str.isascii
    - https://docs.python.org/3/library/stdtypes.html#str.isalpha
    - https://docs.python.org/3/library/stdtypes.html#str.islower
- ord 関数も使えそうです。
    - https://docs.python.org/3/library/functions.html#ord

```python

class Solution:
    def is_lowercase_english_letters(self, letters):
        for letter in letters:
            if ord(letter) < ord('a') or ord('z') < ord(letter):
                return False
        return True

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_letters_to_anagrams = {}
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            sorted_letters = "".join(sorted(letters))
            if sorted_letters not in sorted_letters_to_anagrams:
                sorted_letters_to_anagrams[sorted_letters] = []
            sorted_letters_to_anagrams[sorted_letters].append(letters)
        return [anagrams for anagrams in sorted_letters_to_anagrams.values()]

```

- all 関数が読みやすいかもしれません
    - https://docs.python.org/3/library/functions.html#all

```python

class Solution:
    def is_lowercase_english_letters(self, letters):
        return all(ord('a') <= ord(letter) <= ord('z') for letter in letters)

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_letters_to_anagrams = {}
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            sorted_letters = "".join(sorted(letters))
            if sorted_letters not in sorted_letters_to_anagrams:
                sorted_letters_to_anagrams[sorted_letters] = []
            sorted_letters_to_anagrams[sorted_letters].append(letters)
        return [anagrams for anagrams in sorted_letters_to_anagrams.values()]

```

### 追記 string.ascii_lowercase

```python

class Solution:
    def is_lowercase_english_letters(self, letters):
        return all(letter in string.ascii_lowercase for letter in letters)

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_letters_to_anagrams = {}
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            sorted_letters = "".join(sorted(letters))
            if sorted_letters not in sorted_letters_to_anagrams:
                sorted_letters_to_anagrams[sorted_letters] = []
            sorted_letters_to_anagrams[sorted_letters].append(letters)
        return [anagrams for anagrams in sorted_letters_to_anagrams.values()]

```

- a と z を明示している分 個人的に ord 関数を使った方が読みやすい気がします。
- isascii, isalpha, islower は何か知らない動きをしそうだったので、もう少し調べたうえで使ってみようと思います。
- 復習のときに文字列関数の実装も見ようと思います。

## Step2

### 発想を調べたり、コードを読む

- https://github.com/kazukiii/leetcode/pull/13/files
    - 辞書のキーに単語の各文字の個数を配列に入れたものを使う方法もありました。これも書いてみようと思います。
- https://discord.com/channels/1084280443945353267/1337642831824814192/1344303950257721365
    - 想定しないものが来たときに「何が起きるか」という視点を持つ。英小文字以外にどんなものがあるのか、整理しておいた方がよさそうです。
- https://github.com/Fuminiton/LeetCode/pull/12#discussion_r1971612972
    - 想定できるシナリオ自体を広くしていくこと。これに関してはあまり好みで考えない方がいいかもしれない。
- https://github.com/ichika0615/arai60/pull/11/files#r1975258630
    - ascii_lowercase というものもある。
        - https://docs.python.org/3/library/string.html#string.ascii_lowercase
- https://github.com/fhiyo/leetcode/pull/15/files
    - ソートした文字列を変数に置かなくても読みやすいかもしれない。これは変数名が短く整えられているからかな？
- https://github.com/TORUS0818/leetcode/pull/14/files
    - もしかして内法表記使う人の方が少ないですかね。
- https://github.com/katataku/leetcode/pull/11
    - join と tuple の選択で、tuple でも、という温度感なのですね。
- https://github.com/HitoshiKoba/Arai60-public/pull/5/files#r2020661663
    - Unicode のサロゲートペアや結合文字というものもあるらしい。これは本当に大変なものとのこと。
- https://github.com/plushn/SWE-Arai60/pull/12
    - 自分は考えなかったですが、ValueError もありますね。もう少し広く見ないとですね。

### 書き換え

- letters を使っているので、letter を使わないとと思っていましたが、c の方が読みやすいかもしれません。
- メインループの中に if 文が複数ある場合は、defaultdict を使った方が読みやすく感じました。

```python

class Solution:
    def is_lowercase_english_letters(self, letters):
        if not letters:
            return False
        return all(ord('a') <= ord(c) <= ord('z') for c in letters)

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_letters_to_anagrams = defaultdict(list)
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            sorted_letters = "".join(sorted(letters))
            sorted_letters_to_anagrams[sorted_letters].append(letters)
        return [anagrams for anagrams in sorted_letters_to_anagrams.values()]

```

- 文字列の各文字の個数を数えて、それをグループのキーにする方法を試します。

- 頭の中で勝手に、辞書がキー順にソートされているイメージを作ってしまっていました。挿入順を保証するということと変な感じで混ざってしまっていたので注意します。

```python

# このコードは正しい結果を返しません
class Solution:
    def is_lowercase_english_letters(self, letters):
        return all(ord('a') <= ord(c) <= ord('z') for c in letters)

    def get_frequency(self, letters):
        frequency = defaultdict(int)
        for c in letters:
            frequency[c] += 1
        return tuple(frequency.items())

    def groupAnagrams(self, strs):
        frequency_to_anagrams = defaultdict(list)
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            frequency = self.get_frequency(letters)
            frequency_to_anagrams[frequency].append(letters)
        return [anagrams for anagrams in frequency_to_anagrams.values()]

```

- tuple を使うなら sort が必要かな。
- frozenset なら sort せずにも書ける。set は unhashable なので注意。
    - https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset
        > The set type is mutable — the contents can be changed using methods like add() and remove(). Since it is mutable, it has no hash value and cannot be used as either a dictionary key or as an element of another set
- tuple, set, frozenset の関係性に注意。

```python

class Solution:
    def is_lowercase_english_letters(self, letters):
        return all(ord('a') <= ord(c) <= ord('z') for c in letters)

    def get_frequency(self, letters):
        frequency = defaultdict(int)
        for c in letters:
            frequency[c] += 1
        return frozenset(frequency.items())

    def groupAnagrams(self, strs):
        frequency_to_anagrams = defaultdict(list)
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            frequency = self.get_frequency(letters)
            frequency_to_anagrams[frequency].append(letters)
        return [anagrams for anagrams in frequency_to_anagrams.values()]

```

- 辞書ではなくリストを使うこともできる。

```python

class Solution:
    def is_lowercase_english_letters(self, letters):
        return all(ord('a') <= ord(c) <= ord('z') for c in letters)

    def get_frequency(self, letters):
        frequency = [0] * 26
        for c in letters:
            frequency[ord(c) - ord('a')] += 1
        return tuple(frequency)

    def groupAnagrams(self, strs):
        frequency_to_anagrams = defaultdict(list)
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            frequency = self.get_frequency(letters)
            frequency_to_anagrams[frequency].append(letters)
        return [anagrams for anagrams in frequency_to_anagrams.values()]

```

- Counter を使うのもいいかもです。存在しないキーにアクセスすると、Keyerror ではなく、0を返します。
- https://docs.python.org/3/library/collections.html#collections.Counter
    > Counter objects have a dictionary interface except that they return a zero count for missing items instead of raising a KeyError:

```python

class Solution:
    def is_lowercase_english_letters(self, letters):
        return all(ord('a') <= ord(c) <= ord('z') for c in letters)

    def groupAnagrams(self, strs):
        frequency_to_anagrams = defaultdict(list)
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            frequency = frozenset(Counter(letters).items())
            frequency_to_anagrams[frequency].append(letters)
        return [anagrams for anagrams in frequency_to_anagrams.values()]

```

## Step3

- https://github.com/irohafternoon/LeetCode/pull/14
    - 辞書の変数名の付け方について、ここで議論されている grouped_anagrams を参考にしました。
- こちらで練習しました。

```python

class Solution:
    def is_lowercase_english_letters(self, letters: str) -> bool:
        return all(ord('a') <= ord(c) <= ord('z') for c in letters)

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        grouped_anagrams = defaultdict(list)
        for letters in strs:
            if not self.is_lowercase_english_letters(letters):
                continue
            sorted_letters = "".join(sorted(letters))
            grouped_anagrams[sorted_letters].append(letters)
        return [anagrams for anagrams in grouped_anagrams.values()]

```

## 感想

- ちょっとした書き換えのつもりでもドキュメントに目を通しておかないとなと思えたことが収穫でした。