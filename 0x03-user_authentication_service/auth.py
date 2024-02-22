#!/usr/bin/env python3


"""
hashing
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    encoded_pass = password.encode('utf-8')
    salt = bcrypt.gensalt()
    my_hash = bcrypt.hashpw(encoded_pass, salt)
    return my_hash
