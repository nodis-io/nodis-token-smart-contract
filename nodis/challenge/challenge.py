from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Notify, Serialize, Deserialize
from utils import concat_bytes
from tracker import create_tracker

def generate_challenge_key(owner, challenge_id):
    return concat_bytes(['Challenge{owner:String=',owner,';challenge:Number=',challenge_id,'}'])

def open_challenge(ctx, owner, challenge_id, balance):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    challenge['state'] = 'OPEN'
    challenge['balance'] = balance
    put(ctx, challenge_key, challenge)
    return challenge_key

def close_challenge(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    challenge['state'] = 'CLOSED'
    tracker = get_tracker(ctx, challenge['tracker_key'])
    challenge['winners'] = tracker
    put(ctx, challenge_key, challenge)
    return challenge_key

def put(ctx, challenge_key, challenge):
    to_save = Serialize(challenge)
    Put(ctx, challenge_key, to_save) # 1 GAS
    return True

def get_challenge(ctx, challenge_key):
    to_retrieve = Get(ctx, challenge_key)
    return Deserialize(to_retrieve)

def create_challenge(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = {'owner': owner, 
        'cid': challenge_id, 
        'state': 'CREATED', 
        'balance': 0,
        'tracker_key': create_tracker(ctx, owner, challenge_id)}
    put(ctx, challenge_key, challenge)
    return challenge_key

def get_tracker_key(ctx, challenge_key):
    challenge = get_challenge(ctx, challenge_key)
    return challenge['tracker_key']

def get_challenge_state(ctx, challenge_key):
    challenge = get_challenge(ctx, challenge_key)
    return challenge['state']

def get_challenge_balance(ctx, challenge_key):
    challenge = get_challenge(ctx, challenge_key)
    return challenge['balance']