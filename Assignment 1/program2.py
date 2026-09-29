import re

def check_password(password):
    # Password length check
    if len(password) < 6 or len(password) > 12:
        return "Invalid: Password must be 6 to 12 characters long."

    # Lowercase letter
    if not re.search(r"[a-z]", password):
        return "Invalid: Must contain at least one lowercase letter."

    # Uppercase letter
    if not re.search(r"[A-Z]", password):
        return "Invalid: Must contain at least one uppercase letter."

    # Digit
    if not re.search(r"[0-9]", password):
        return "Invalid: Must contain at least one number."

    # Special character
    if not re.search(r"[$#@]", password):
        return "Invalid: Must contain at least one special character ($, #, @)."

    return "Valid Password"


# Take password from user
password = input("Enter password: ")

print(check_password(password))