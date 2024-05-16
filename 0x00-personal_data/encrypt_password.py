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