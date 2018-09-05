from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Notify, Serialize, Deserialize
from utils import concat_bytes, contains

def generate_challenge_key(owner, challenge_id):
    return concat_bytes(['Challenge{owner:String=',owner,';challenge:Number=',challenge_id,'}'])

def put(ctx, challenge_key, challenge):
    to_save = Serialize(challenge)
    Put(ctx, challenge_key, to_save)
    return True

def get_challenge(ctx, challenge_key):
    to_retrieve = Get(ctx, challenge_key)
    return Deserialize(to_retrieve)

def create_challenge(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = {
        'owner': owner, 
        'cid': challenge_id, 
        'state': 'OPEN', 
        'submissions': [],
        'timestamp': 0
    }
    put(ctx, challenge_key, challenge)
    return challenge_key

def submit(ctx, challenge_key, submission_key):
    challenge = get_challenge(ctx, challenge_key)
    if contains(challenge['submissions'], submission_key):
        return False
    elif len(challenge['submissions'])<100:
        challenge['submissions'].append(submission_key)
        put(ctx, challenge_key, challenge)
        return True
    else:
        challenge['state'] = 'CLOSED'
        return False

def close_challenge(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    if challenge['state'] != 'CLOSED':
        challenge['state'] = 'CLOSED'
        status = put(ctx, challenge_key, challenge)
    return challenge_key

def is_closed(ctx, challenge_key):
    challenge = get_challenge(ctx, challenge_key)
    return challenge['state'] == 'CLOSED'
    
