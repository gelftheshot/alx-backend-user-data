#!/usr/bin/env python3
""" a fucntion to hash a password """
import bcrypt


def hash_password(password: str) -> bytes:
    '''
        checking if a password is hashed
    '''
    pass_encoded = password.encode()
    pass_hashed = bcrypt.hashpw(pass_encoded, bcrypt.gensalt())

    return pass_hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
       Use bcrypt to validate that the provided password matches the hashed
       password.
    '''
    valid = False
    pass_encoded = password.encode()
    if bcrypt.checkpw(pass_encoded, hashed_password):
        valid = True
    return valid
