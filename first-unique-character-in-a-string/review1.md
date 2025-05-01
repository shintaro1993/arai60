# 復習や宿題を整理する用です。

## いただいたレビューコメントをもとに Step3 のコードを修正

```python

class Solution:
    def normalize(self, email):
        local, domain = email.split("@")
        local = local.replace(".", "")
        start_to_ignore = local.find("+")
        if start_to_ignore == -1:
            start_to_ignore = len(local)
        return f"{local[:start_to_ignore]}@{domain}"

    def is_valid_characters(self, email):
        return all(ord("a") <= ord(c) <= ord("z") or c in ".+@" for c in email)

    def is_valid_email(self, email):
        if not email or not self.is_valid_characters(email):
            return False
        if email.count("@") != 1:
            return False
        local, domain = email.split("@")
        if not local:
            return False
        if not domain.removesuffix(".com"):
            return False
        if local.startswith("+"):
            return False
        if not domain.endswith(".com"):
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

- 書く時間は短縮しました。