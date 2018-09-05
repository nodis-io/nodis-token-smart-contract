from boa.interop.Neo.Storage import *
from boa.builtins import concat

def generate_challenge_key(address):
    return concat(b'Business:',address)

def register(ctx, address):
    key = generate_challenge_key(address)
    status = Put(ctx, key)
    return True

def check(ctx, address):
    key = generate_challenge_key(address)
    status = Get(ctx, key)
    return status

def signout(ctx, address):
    key = generate_challenge_key(address)
    Delete(ctx, address)
    return True