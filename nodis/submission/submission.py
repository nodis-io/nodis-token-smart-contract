from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import Notify, Serialize, Deserialize, Log
from utils import concat_bytes, contains
from nodis.challenge.challenge import submit, get_challenge, is_closed, generate_challenge_key

def put(ctx, submission_key, submission):
    to_save = Serialize(submission)
    Put(ctx, submission_key, to_save)
    return True

def get_submission(ctx, submission_key):
    to_retrieve = Get(ctx, submission_key)
    if to_retrieve:  
        submission = Deserialize(to_retrieve)
        return submission
    return False

def generate_submission_key(challenger, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    key = concat_bytes(['Submission{user:ByteArray=',challenger,';challenge:Key=',challenge_key,'}'])
    return key

def create_submission(ctx, challenger, owner, challenge_id):
    challenge_key = generate_challenge_key(owner, challenge_id)
    Log("Generating challenge key.")
    Log(challenge_key)
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    Log("Generating submission key.")
    Log(submission_key)
    Log("Initiating a new submission.")
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
        Log("Storing submission.")
        put(ctx, submission_key, submission)
        return submission_key
    else:
        Log("Submission was not saved.")
        return False

def approve(ctx, voter, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    Log("Generating submission key.")
    Log(submission_key)
    submission = get_submission(ctx, submission_key)
    voters = submission['voters']
    voted = contains(voters, voter)
    Log("Checking that the user has not already voted for this submission.")
    Log(voted)
    if voted == False:
        Log("Approving submission.")
        approvers = submission['approvers']
        voters.append(voter)
        approvers.append(voter)
        submission['voters'] = voters
        submission['approvers'] = approvers
        submission['difference'] = len(submission['approvers']) - len(submission['rejecters'])
        submit(ctx, submission['challenge_key'], submission_key)
        if submission['difference'] >= 0 and len(submission['approvers']) > 0:
            submission['status'] = 'APPROVED'
        elif submission['difference'] < 0:
            submission['status'] = 'REJECTED'
        put(ctx, submission_key, submission)
        return True
    else:
        Log("The user already voted.")
        return False

def reject(ctx, voter, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    Log("Generating submission key.")
    Log(submission_key)
    submission = get_submission(ctx, submission_key)
    voters = submission['voters']
    voted = contains(voters, voter)
    Log("Checking that the user has not already voted for this submission.")
    Log(voted)
    if voted == False:
        Log("Rejecting submission.")
        rejecters = submission['rejecters']
        voters.append(voter)
        rejecters.append(voter)
        submission['voters'] = voters
        submission['rejecters'] = rejecters
        submission['difference'] = len(submission['approvers']) - len(submission['rejecters'])
        submit(ctx, submission['challenge_key'], submission_key)
        if submission['difference'] >= 0 and len(submission['approvers']) > 0:
            submission['status'] = 'APPROVED'
        elif submission['difference'] < 0:
            submission['status'] = 'REJECTED'
        put(ctx, submission_key, submission)
        return True
    else:
        Log("The user already voted.")
        return False


def promoter_fund_claim(ctx, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    Log("Generating submission key.")
    Log(submission_key)
    submission = get_submission(ctx, submission_key)
    challenge_key = generate_challenge_key(owner, challenge_id)
    Log("Generating challenge key.")
    Log(challenge_key)
    if is_closed(ctx, challenge_key):
        Log("Challenge is closed.")
        if submission['status'] == 'APPROVED':
            Log("Submission has been approved. Eligible for claim.") 
            if submission['claimed'] == 'NO':
                Log("Reward has not been claimed. Mining...")
                submission['claimed'] = 'YES'
                put(ctx, submission_key, submission)
                return True
            else:
                Log("Reward has already been claimed.")
                return False
        else:
            Log("Submission has been rejected. Not eligible for claim.") 
            return False
    else:
        Log("Challenge is still open.")
        return False

def rejecter_fund_claim(ctx, voter, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    Log("Generating submission key.")
    Log(submission_key)
    submission = get_submission(ctx, submission_key)
    rejecters = submission['rejecters']
    rejecter = contains(rejecters, voter)
    if is_closed(ctx, submission['challenge_key']):
        Log("Challenge is closed.")
        if rejecter != False:
            Log("Voter rejected the submission.") 
            if submission['status'] == 'REJECTED':
                Log("Submission was rejected. Voter is eligible for claim.")
                rejecters.remove(rejecter[voter])
                submission['rejecters'] = rejecters
                put(ctx, submission_key, submission)
                Log("Voter has been removed from the rejecter list. Claim can proceed.")
                return len(rejecters)
            else:
                Log("Submission was not rejected.") 
                return False
        else:
            Log("Voter is not in the rejecter list.") 
            return False
    else:
        Log("Challenge is still open.")
        return False

def approver_fund_claim(ctx, voter, challenger, owner, challenge_id):
    submission_key = generate_submission_key(challenger, owner, challenge_id)
    Log("Generating submission key.")
    Log(submission_key)
    submission = get_submission(ctx, submission_key)
    approvers = submission['approvers']
    approver = contains(approvers, voter)
    if is_closed(ctx, submission['challenge_key']):
        Log("Challenge is closed.")
        if approver != False:
            Log("Voter approved the submission.")  
            if submission['status'] == 'APPROVED':
                Log("Submission was approved. Voter is eligible for claim.")
                approvers.remove(approver[voter])
                submission['approvers'] = approvers
                put(ctx, submission_key, submission)
                Log("Voter has been removed from the approver list. Claim can proceed.")
                return len(approvers)
            else:
                Log("Submission was not approved.") 
                return False
        else:
            Log("Voter is not in the approver list.")
            return False
    else:
        Log("Challenge is still open.")
        return False