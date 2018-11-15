from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Log, Serialize, Deserialize
from utils import concat_bytes, contains

def generate_challenge_key(owner, challenge_id):
    return concat_bytes(['Challenge{owner:String=',owner,';challenge:Number=',challenge_id,'}'])

def put(ctx, challenge_key, challenge):
    Log("Storing challenge.")
    to_save = Serialize(challenge)
    Put(ctx, challenge_key, to_save)
    return True

def get_challenge(ctx, challenge_key):
    Log("Retrieving challenge.")
    to_retrieve = Get(ctx, challenge_key)
    if to_retrieve:
        challenge = Deserialize(to_retrieve)
        return challenge
    return False

def create_challenge(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    Log("Generating challenge key.")
    Log(challenge_key)
    if not get_challenge(ctx, challenge_key):
        Log("Challenge does not already exist. Initiating a new challenge.")
        challenge = {
            'owner': owner, 
            'cid': challenge_id, 
            'state': 'OPEN', 
            'submissions': [],
            'timestamp': 0
        }
        put(ctx, challenge_key, challenge)
        return challenge_key
    else:
        Log("Challenge key already exists.")
        return False

def submit(ctx, challenge_key, submission_key):
    challenge = get_challenge(ctx, challenge_key)
    if challenge['state'] == 'OPEN':
        submissions = challenge['submissions']
        if contains(submissions, submission_key):
            Log("Submission already exists.")
            return False
        elif len(submissions)<100:
            Log("Adding new submission.")
            submissions.append(submission_key)
            challenge['submissions'] = submissions
            put(ctx, challenge_key, challenge)
            return True
        else:
            Log("The maximum number of submissions for this challenge has been reached.")
            challenge['state'] = 'CLOSED'
            put(ctx, challenge_key, challenge)
            return False
    else:
        return False

def close_challenge(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    if challenge['state'] != 'CLOSED':
        challenge['state'] = 'CLOSED'
        put(ctx, challenge_key, challenge)
        Log("Challenge closed.")
    return challenge_key

def is_closed(ctx, challenge_key):
    challenge = get_challenge(ctx, challenge_key)
    return challenge['state'] == 'CLOSED'