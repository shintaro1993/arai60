```python

class Solution:
    def is_valid_letters(self, letters):
        allowed_special_letter = {".", "+", "@"}
        return all(
            ord("a") <= ord(c) <= ord("z") or c in allowed_special_letter for c in letters
        )

    def get_formed_email(self, email):
        if not email or not self.is_valid_letters(email):
            return None
        if email.count("@") >= 2:
            return None
        local, domain = email.split("@")
        if local.startswith("+") or not local:
            return None
        if not domain.endswith(".com") or not domain[:-4]:
            return None
        local = local.replace(".", "")
        start_to_ignore = local.find("+")
        if start_to_ignore == -1:
            start_to_ignore = len(local)
        return "".join([local[:start_to_ignore], "@", domain])

    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()
        for email in emails:
            formed_email = self.get_formed_email(email)    
            if formed_email is None:
                continue
            unique_emails.add(formed_email)
        return len(unique_emails)

```