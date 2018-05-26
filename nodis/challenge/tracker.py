from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Notify, Serialize, Deserialize
from nodis.utils import concat_bytes, sort

def generate_key(challenge_id):
    return concat_bytes(['owner:String=',owner,';challenge:Number='challenge_id])

def create(ctx, challenge_id, challenge_id):
    tracker = {}
    to_save = Serialize(tracker)
    tracker_key = generate_key(owner, challenge_id)
    lowest_key = generate_key(owner, challenge_id)
    Put(ctx, key, to_save) # 1 GAS

def put(ctx, tracker):
    pass

def get(ctx, tracker):
    pass

def get_lowest_key(tracker):
    pass

def remove(tracker, key):
    new_dict = {}
    for k in tracker.keys():
        if k != key:
            new_dict[k] = tracker[k]
    return new_dict

def update_tracker(tracker, key, value):
    lowest_key = get_lowest_key(tracker)
    if has_key(tracker, key):
        tracker[key] = value
    elif len(tracker.keys())<50:
        tracker[key] = value
    elif value > tracker[lowest_key]:
        remove(tracker, lowest_key)
        tracker[key] = value
    else:
        return tracker
