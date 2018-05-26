from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Notify, Serialize, Deserialize
from nodis.utils import concat_bytes

def generate_key(owner, challenge_id):
    return concat_bytes(['owner:String=',owner,';challenge:Number='challenge_id])

def create(ctx, owner, challenge_id):
    challenge = {'owner': owner, 'cid': challenge_id, 'state': 'NULL', 'balance': 0}
    to_save = Serialize(challenge)
    key = generate_key(owner, challenge_id)
    Put(ctx, key, to_save) # 1 GAS

def open(ctx, owner, challenge_id, balance):
    key = generate_key(owner, challenge_id)
    to_retrieve = Get(ctx, key) # 0.1 GAS
    challenge = Deserialize(to_retrieve)
    challenge['state'] = 'OPEN'
    challenge['balance'] = balance
    to_save = Serialize(challenge)
    Put(ctx, key, to_save) # 1 GAS

def close():
    key = generate_key(owner, challenge_id)
    to_retrieve = Get(ctx, key) # 0.1 GAS
    challenge = Deserialize(to_retrieve)
    challenge['state'] = 'CLOSED'
    challenge['balance'] = balance

def delete():
    pass