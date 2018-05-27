from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Notify, Serialize, Deserialize
from utils import concat_bytes

def generate_tracker_key(owner, challenge_id):
    return concat_bytes(['Tracker{owner:String=',owner,';challenge:Number=',challenge_id,'}'])

def put(ctx, tracker_key, tracker):
    to_save = Serialize(tracker)
    Put(ctx, tracker_key, to_save) # 1 GAS
    return True

def get_tracker(ctx, tracker_key):
    to_retrieve = Get(ctx, tracker_key)
    return Deserialize(to_retrieve)

def get_lowest_key(tracker):
    lowest_votes = 1000000000
    lowest_key = ''
    for key in tracker.keys():
        if lowest_votes > tracker[key]:
            lowest_votes = tracker[key]
            lowest_key = key
    return lowest_key        

def remove(tracker, key):
    new_dict = {}
    for k in tracker.keys():
        if k != key:
            new_dict[k] = tracker[k]
    return new_dict

def create_tracker(ctx, owner, challenge_id):
    tracker_key = generate_tracker_key(owner, challenge_id)
    tracker = {}
    put(ctx, tracker_key, tracker)
    return tracker_key

def update_tracker(tracker, key, value):
    lowest_key = get_lowest_key(tracker)
    if has_key(tracker, key):
        tracker[key] = value
        return tracker
    elif len(tracker.keys())<50:
        tracker[key] = value
        return tracker
    elif value > tracker[lowest_key]:
        new_tracker = remove(tracker, lowest_key)
        new_tracker[key] = value
        return new_tracker
    else:
        return tracker