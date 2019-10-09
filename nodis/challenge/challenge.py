from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Log, Serialize, Deserialize, GetTime
from utils import concat_bytes, contains

def generate_challenge_key(owner, challenge_id):
    return concat_bytes(['C{O=',owner,'&I=',challenge_id,'}'])

def set_challenge(ctx, challenge_key, challenge):
    Log("Storing challenge.")
    to_save = Serialize(challenge)
    Put(ctx, challenge_key, to_save)
    return True

def last_challenge_timestamp(ctx, owner):
    key = concat('Last_Challenge_',owner)
    timestamp = Get(ctx, key)
    if timestamp:
        return timestamp
    else:
        return 0

def update_last_challenge_date(ctx, owner, timestamp):
    key = concat('Last_Challenge_',owner)
    Put(ctx, key, timestamp)
    return True

def check_challenge_package(ctx, owner):
    key = concat('Challenge_Package_', owner)
    challenges = Get(ctx, key)
    if challenges:
        return challenges
    else:
        return 0

def buy_challenge_package(ctx, owner, new_challenges):
    key = concat('Challenge_Package_', owner)
    challenges = check_challenge_package(ctx, owner)
    number_challenges = challenges + new_challenges
    Put(ctx, key, number_challenges)
    return number_challenges

def decrement_challenge_package(ctx, owner):
    key = concat('Challenge_Package_', owner)
    challenges = check_challenge_package(ctx, owner)
    number_challenges = challenges - 1
    Put(ctx, key, number_challenges)
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
    last_challenge_date = last_challenge_timestamp(ctx, owner)
    challenge_package = check_challenge_package(ctx, owner)
    using_package = False
    can_create_challenge = True

    if GetTime() > last_challenge_date + 2592000:
        can_create_challenge = True
        Log("The business can create a challenge.")
    elif challenge_package > 0:
        can_create_challenge = True
        using_package = True
        Log("The business has created a challenge in the past 30 days. Using challenge package.")
    else:
        Log("The last challenge created by the business was less than 30 days ago.")
        Log("The business challenge package is empty.")
    
    if can_create_challenge:
        if not get_challenge(ctx, challenge_key):
            Log("Challenge does not already exist. Initiating a new challenge.")
            challenge = {
                'owner': owner, 
                'cid': challenge_id, 
                'state': 'OPEN', 
                'submissions': [],
                'timestamp': GetTime()
            }
            set_challenge(ctx, challenge_key, challenge)
            update_last_challenge_date(ctx, owner, challenge['timestamp'])
            if using_package:
                decrement_challenge_package(ctx, owner)
            return True
        else:
            Log("Challenge key already exists.")
            return False
    else:
        Log("The business cannot create a challenge at the moment.")
        return False


def submit(ctx, challenge_key, submission_key):
    challenge = get_challenge(ctx, challenge_key)
    if challenge:
        Log("Challenge exists.")
        if challenge['state'] == 'OPEN':
            Log("Challenge is open")
            submissions = challenge['submissions']
            if contains(submissions, submission_key):
                Log("Submission already exists.")
                return False
            else:
                Log("Adding new submission.")
                submissions.append(submission_key)
                challenge['submissions'] = submissions
                set_challenge(ctx, challenge_key, challenge)
                return True
        else:
            Log("Challenge is closed")
            return False
    Log("This challenge does not exist.")
    return False

def close_challenge(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    if challenge:
        if challenge['state'] != 'CLOSED':
            challenge['state'] = 'CLOSED'
            set_challenge(ctx, challenge_key, challenge)
            Log("Challenge closed.")
        return True
    Log("This challenge does not exist.")
    return False

def is_challenge_closed(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    if challenge:
        return challenge['state'] == 'CLOSED'
    Log("This challenge does not exist.")
    return False

def is_challenge_open(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    if challenge:
        return challenge['state'] == 'OPEN'
    Log("This challenge does not exist.")
    return False

def submission_number(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    if challenge:
        return len(challenge['submissions'])
    Log("This challenge does not exist.")
    return False

def challenge_expiry_date(ctx, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    challenge = get_challenge(ctx, challenge_key)
    if challenge:
        return challenge['timestamp'] + 1209600
    Log("This challenge does not exist.")
    return False