# 929. Unique Email Addresses

## Step1

- 一部の処理が重複するかもしれませんが、有効なメールアドレスかどうか調べることと、メールアドレスの変形作業を分けたいと思いました。

```python

class Solution:
    def get_formed_email(self, email):
        local, domain = email.split("@")
        local = local.replace(".", "")
        start_to_ignore = local.find("+")
        if start_to_ignore == -1:
            start_to_ignore = len(local)
        return "".join([local[:start_to_ignore], "@", domain])

    def is_valid_letters(self, letters):
        allowed_special_letter = {".", "+", "@"}
        return all(
            ord("a") <= ord(c) <= ord("z") or c in allowed_special_letter for c in letters
        )

    def is_valid_email(self, email):
        if not email or not self.is_valid_letters(email):
            return False
        if email.count("@") >= 2:
            return False
        local, domain = email.split("@")
        if local.startswith("+") or not local:
            return False
        if not domain.endswith(".com") or not domain[:-4]:
            return False
        return True

    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()
        for email in emails:
            if not self.is_valid_email(email):
                continue
            formed_email = self.get_formed_email(email)    
            unique_emails.add(formed_email)
        return len(unique_emails)

```

- 無効なアドレスを発見した場合、それは除いて処理を続けるのが親切かと思いました。
    - 追記：ユースケースを考えて、ユースケースごとにどうするとよさそうかも考えていく。
- is_valid_letters 関数の書き比べです。個人的には好みかなと思っています。

```python

    def is_valid_letters(self, letters):
        allowed_special_letters = {".", "+", "@"}
        for c in letters:
            if ord("a") <= ord(c) <= ord("z"):
                continue
            if c in allowed_special_letters:
                continue
            return False
        return True

    def is_valid_letters(self, letters):
        allowed_special_letters = {".", "+", "@"}
        return all(
            ord("a") <= ord(c) <= ord("z") or c in allowed_special_letters for c in letters
        )

```

- 全体の構成の変化として、is_valid_email 関数をなくして、get_formed_email 関数で無効なメールアドレスも調べて、見つけたら None を返す、というのもありかなと思いました。practice.md に書いてみました。

- 見積り
    - n：emails の長さ
    - m：emails[i] の長さ
    - 時間計算量：O(n * m)
    - 空間計算量：O(n * m)

## Step2

### 調べたこと

- https://discord.com/channels/1084280443945353267/1200089668901937312/1207996784211918899
    - キーワード：ステートマシン、オートマトン、チョムスキー階層、type-3、正規文法
    - rsplit と maxsplit を調べていなかったのでここで見ておく
        - https://docs.python.org/3/library/stdtypes.html#str.rsplit
        - https://docs.python.org/3/library/stdtypes.html#str.rsplit
- https://github.com/colorbox/leetcode/pull/28#discussion_r1844942851
    - 自分が変形と呼んでいたものは、「正規化」と呼ぶらしい
- https://github.com/SuperHotDogCat/coding-interview/pull/30#discussion_r1646552062
    - RFC でメールアドレスの仕様を確認しよう

- 確認しておく
    - [How can I validate an email address using a regular expression?](https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression/201378#201378)
    - [Internet Message Format](https://datatracker.ietf.org/doc/html/rfc5322)

### 読んだコード

- https://github.com/hayashi-ay/leetcode/pull/25
    - オートマトンで書かれたコード読みにくいのかなと思いましたが、continue の処理が意外と読みやすいです。ただ書くのは大変そうです。正規表現も、簡単なものから練習していこうと思います。
- https://github.com/seal-azarashi/leetcode/pull/14/files
    - 並列化というのも考えているのですね。
- https://github.com/t0hsumi/leetcode/pull/14/files
    - is_valid 関数の中だからか、 if 文が縦に増えていってもあまり違和感はないかもですね。
- https://github.com/plushn/SWE-Arai60/pull/14/files
    - 文字数制限のことまで調べられていた。自分は 入力が空でもなく、@ が1つもない場合を考えられていなかった。また @ が複数あってもいい場合があるらしく、改めて RFC を読んでから実装してみよう。あと、もう少し不正なケースを考えて試す必要がある。

```python

class Solution:
    def normalize(self, email: str) -> str:
        local, domain = email.split("@")
        local = local.replace(".", "")
        start_to_ignore = local.find("+")
        if start_to_ignore == -1:
            start_to_ignore = len(local)
        return "".join([local[:start_to_ignore], "@", domain])

    def is_valid_characters(self, characters: str) -> bool:
        SPECIAL_CHARACTERS = {".", "+", "@"}
        return all(
            ord("a") <= ord(c) <= ord("z") or c in SPECIAL_CHARACTERS for c in characters
        )

    def is_valid_email(self, email: str) -> bool:
        AT_SIGN = "@"
        INVALID_PREFIX = "+"
        VALID_SUFFIX = ".com"
        if not email or not self.is_valid_characters(email):
            return False
        if email.count(AT_SIGN) != 1:
            return False
        local, domain = email.split(AT_SIGN)
        if local.startswith(INVALID_PREFIX) or not local:
            return False
        if not domain.endswith(VALID_SUFFIX) or not domain[:-len(VALID_SUFFIX)]:
            return False
        return True

    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()
        for email in emails:
            if not self.is_valid_email(email):
                continue
            normalized_email = self.normalize(email)    
            unique_emails.add(normalized_email)
        return len(unique_emails)

```

- is_valid_email 関数では処理の意図を伝えるために定数にしました。RFC で `at-sign` や `special characters` などの言葉が使われていたので定数名で使いました。normalize 関数の中でも `+` などを定数にしようとしましたが is_valid_email 関数の中での意味と異なることに気づきやめました。

## Step3

- 今までで一番 step3 で苦労しました。何かを落ちないようにしようとすると、別の何かが落ち続けました。自分のリソースが限られていることを実感しました。

- 現状以下のコードに落ち着きました。復習をするときに改めて、RFC を調べてみます。

```python

class Solution:
    def normalize(self, email):
        local, domain = email.split("@")
        local = local.replace(".", "")
        start_to_ignore = local.find("+")
        if start_to_ignore == -1:
            start_to_ignore = len(local)
        return "".join([local[:start_to_ignore], "@", domain])

    def is_valid_characters(self, email):
        SPECIAL_CHARACTERS = {".", "+", "@"}
        return all(
            ord("a") <= ord(c) <= ord("z") or c in SPECIAL_CHARACTERS for c in email
        )

    def is_valid_email(self, email):
        AT_SIGN = "@"
        INVALID_PREFIX = "+"
        VALID_SUFFIX = ".com"

        if not email or not self.is_valid_characters(email):
            return False
        if email.count(AT_SIGN) != 1:
            return False
        local, domain = email.split(AT_SIGN)
        if not local or not domain[:-len(VALID_SUFFIX)]:
            return False
        if local.startswith(INVALID_PREFIX):
            return False
        if not domain.endswith(VALID_SUFFIX):
            return False
        return True

    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()
        for email in emails:
            if not self.is_valid_email(email):
                continue
            normalized_email = self.normalize(email)
            unique_emails.add(normalized_email)
        return len(unique_emails)

```