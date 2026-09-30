# Optimized Password Audit with Pattern Constraints
# Python 3.10+

# Classification:
# STRONG
# WEAK_LENGTH
# WEAK_PATTERN
# COMPROMISED

# Data Structure:
# Trie + Aho-Corasick Algorithm


from collections import deque


class TrieNode:
    """Node of the Trie."""

    def __init__(self):
        self.children = {}
        self.failure = 0
        self.is_end = False


class AhoCorasick:
    """Stores banned words and searches them efficiently."""

    def __init__(self):
        self.nodes = [TrieNode()]

    def add_word(self, word):
        """Insert a banned word into the Trie."""

        current = 0

        for ch in word.lower():

            if ch not in self.nodes[current].children:
                self.nodes[current].children[ch] = len(self.nodes)
                self.nodes.append(TrieNode())

            current = self.nodes[current].children[ch]

        self.nodes[current].is_end = True

    def build(self):
        """Build failure links for Aho-Corasick."""

        queue = deque()

        # Root's children have failure link 0
        for child in self.nodes[0].children.values():
            self.nodes[child].failure = 0
            queue.append(child)

        while queue:

            current = queue.popleft()

            for ch, child in self.nodes[current].children.items():

                queue.append(child)

                failure = self.nodes[current].failure

                while (
                    failure != 0
                    and ch not in self.nodes[failure].children
                ):
                    failure = self.nodes[failure].failure

                if ch in self.nodes[failure].children:
                    self.nodes[child].failure = (
                        self.nodes[failure].children[ch]
                    )
                else:
                    self.nodes[child].failure = 0

                # If the failure state is the end of a banned word,
                # this state also represents a match.
                if self.nodes[
                    self.nodes[child].failure
                ].is_end:
                    self.nodes[child].is_end = True

    def contains_banned_word(self, password):
        """Return True if password contains a banned word."""

        current = 0

        for ch in password.lower():

            while (
                current != 0
                and ch not in self.nodes[current].children
            ):
                current = self.nodes[current].failure

            if ch in self.nodes[current].children:
                current = self.nodes[current].children[ch]
            else:
                current = 0

            if self.nodes[current].is_end:
                return True

        return False


def has_required_characters(password):
    """Check lowercase, uppercase, digit and special character."""

    lower = False
    upper = False
    digit = False
    special = False

    for ch in password:

        if ch.islower():
            lower = True

        elif ch.isupper():
            upper = True

        elif ch.isdigit():
            digit = True

        elif ch in "$#@":
            special = True

    return lower and upper and digit and special


def has_repeated_characters(password):
    """Check whether any character occurs 4 times consecutively."""

    count = 1

    for i in range(1, len(password)):

        if password[i] == password[i - 1]:
            count += 1

            if count > 3:
                return True
        else:
            count = 1

    return False


def classify_password(password, matcher):
    """Classify a password according to the given rules."""

    # Check banned words first
    if matcher.contains_banned_word(password):
        return "COMPROMISED"

    # Check password length
    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    # Check required character types
    if not has_required_characters(password):
        return "WEAK_PATTERN"

    # Check consecutive repeated characters
    if has_repeated_characters(password):
        return "WEAK_PATTERN"

    return "STRONG"


def main():
    """Main function."""

    try:
        # Number of banned words
        b = int(input("Enter number of banned words: "))

        if b < 1 or b > 10000:
            raise ValueError(
                "Number of banned words must be between 1 and 10000."
            )

        matcher = AhoCorasick()

        total_length = 0

        # Read banned words
        print("Enter banned words:")

        for _ in range(b):

            word = input().strip()

            if not word:
                raise ValueError("Banned word cannot be empty.")

            total_length += len(word)

            if total_length > 200000:
                raise ValueError(
                    "Total banned word length cannot exceed 200000."
                )

            matcher.add_word(word)

        # Build failure links
        matcher.build()

        # Number of passwords
        n = int(input("Enter number of passwords: "))

        if n < 1 or n > 100000:
            raise ValueError(
                "Number of passwords must be between 1 and 100000."
            )

        print("Enter passwords:")

        # Classify every password
        for i in range(1, n + 1):

            password = input()

            result = classify_password(
                password,
                matcher
            )

            print(f"{i}: {result}")

    except ValueError as error:
        print("Input Error:", error)


if __name__ == "__main__":
    main()
