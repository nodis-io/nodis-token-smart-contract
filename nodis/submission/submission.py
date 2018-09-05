from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Notify, Serialize, Deserialize
from utils import concat_bytes, contains
from nodis.challenge.challenge import submit, get_challenge, is_closed

def generate_challenge_key(owner, challenge_id):
    return concat_bytes(['Challenge{owner:String=',owner,';challenge:Number=',challenge_id,'}'])

def put(ctx, submission_key, submission):
    to_save = Serialize(submission)
    Put(ctx, submission_key, to_save)
    return True

def get_submission(ctx, submission_key):
    to_retrieve = Get(ctx, submission_key)
    return Deserialize(submission_key)

def generate_submission_key(challenger, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    return concat_bytes(['Submission{user:ByteArray=',challenger,';challenge:Key=',challenge_key,'}'])

def create_submission(ctx, challenger, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    submission = {
        'challenger': challenger, 
        'challenge_key': challenge_key, 
        'voters': [],
        'difference': 0,
        'approvers': [],
        'rejecters': [],
        'status': 'SUBMITTED',
        'claimed': 'NO'
    }
    status = submit(ctx, challenge_key, submission_key)
    if status:
        put(ctx, submission_key, submission)
        return submission_key
    return False

def approve(ctx, voter, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    submission = get_submission(ctx, submission_key)
    voted = contains(submission['voters'], voter)
    if not voted:
        submission['voters'].append(voter)
        submission['approvers'].append(voter)
        submission['difference'] = len(submission['approvers']) - len(submission['rejecters'])
        submit(ctx, submission['challenge_key'], submission_key, submission['difference'])
        if submission['difference'] >= 0 and len(submission['approvers']) > 0:
            submission['status'] = 'APPROVED'
        elif submission['difference'] < 0:
            submission['status'] = 'REJECTED'
        put(ctx, submission_key, submission)
        return True
    return False

def reject(ctx, voter, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    submission = get_submission(ctx, submission_key)
    voted = contains(submission['voters'], voter)
    if not voted:
        submission['voters'].append(voter)
        submission['rejecters'].append(voter)
        submission['difference'] = len(submission['approvers']) - len(submission['rejecters'])
        submit(ctx, submission['challenge_key'], submission_key, submission['difference'])
        if submission['difference'] >= 0 and len(submission['approvers']) > 0:
            submission['status'] = 'APPROVED'
        elif submission['difference'] < 0:
            submission['status'] = 'REJECTED'
        put(ctx, submission_key, submission)
        return True
    return False

def promoter_fund_claim(ctx, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    submission = get_submission(ctx, submission_key)
    if challenge['state'] == 'CLOSED' and submission['claimed']=='NO':
        submission['claimed'] = 'YES'
        put(ctx, submission_key, submission)
        return submission['status'] == 'APPROVED'
    return False

def rejecter_fund_claim(ctx, voter, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    submission = get_submission(ctx, submission_key)
    rejecters = submission['rejecters']
    rejecter = contains(rejecters, voter)
    if is_closed(ctx, submission['challenge_key']):
        if rejecter != False and submission['status'] == 'REJECTED':
            rejecters.remove(rejecter[voter])
            submission['rejecters'] = rejecters
            put(ctx, submission_key, submission)
            return True
        else:
            return False
    else:
        False

def approver_fund_claim(ctx, voter, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    submission = get_submission(ctx, submission_key)
    approvers = submission['approvers']
    approver = contains(approvers, voter)
    if is_closed(ctx, submission['challenge_key']):
        if approver != False and submission['status'] == 'APPROVED':
            approvers.remove(approver[voter])
            submission['approvers'] = approvers
            put(ctx, submission_key, submission)
            return True
        else:
            return False
    else:
        False