"""Run this once to get the value for ADMIN_PASSWORD_HASH in your .env.

    python generate_password_hash.py

Paste the printed hash into .env — never put your plaintext password there.
"""

from getpass import getpass

import bcrypt

if __name__ == "__main__":
    password = getpass("Password to hash: ")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    print(hashed.decode("utf-8"))
