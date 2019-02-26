from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash, GetCallingScriptHash
from boa.interop.Neo.Runtime import CheckWitness, Notify, Log
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat


from nodis.token import *
from nodis.nep5 import do_transfer_from
from nodis.challenge.challenge import create_challenge, submit, close_challenge, check_challenge_package, buy_challenge_package, is_challenge_closed, is_challenge_open, submission_number, challenge_expiry_date
from nodis.submission.submission import create_submission, approve, reject, promoter_fund_claim, rejecter_fund_claim, submission_approver_number, submission_rejecter_number, submission_expiry_date


OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve', 'addr_from', 'addr_to', 'amount')

def generate_business_key(address):
    return concat(b'Business:',address)

def register(ctx, address):
    key = generate_business_key(address)
    Put(ctx, key, b'1')
    return True

def check(ctx, address):
    key = generate_business_key(address)
    status = Get(ctx, key)
    return status == b'1'

def signout(ctx, address):
    key = generate_business_key(address)
    Delete(ctx, key)
    return True

def handle_mining(ctx, operation, args):

    Log(operation)

    if operation == 'register_business':
        address = args[0]
        if CheckWitness(TOKEN_OWNER):
            status = register(ctx, address)
            return status
        else:
            return False

    if operation == 'check_business':
        address = args[0]
        status = check(ctx, address)
        return status

    if operation == 'signout_business':
        address = args[0]
        if CheckWitness(TOKEN_OWNER):
            status = signout(ctx, address)
            return status
        else:
            return False

    if operation == 'challenge_reserve':
        return Get(ctx, CHALLENGE_SYSTEM_RESERVE)

    if operation == 'get_mining_rate':
        rate = get_mining_rate(ctx)
        return rate

    if operation == 'get_promoter_mining_rate':
        rate = get_promoter_mining_rate(ctx)
        return rate

    if operation == 'get_approver_mining_rate':
        rate = get_approver_mining_rate(ctx, args[0])
        return rate

    if operation == 'get_rejecter_mining_rate':
        rate = get_rejecter_mining_rate(ctx, args[0])
        return rate

    if operation == 'check_challenge_package':
        owner = args[0]
        Log("Checking challenge package.")
        return check_challenge_package(ctx, owner)

    if operation == 'buy_challenge_package':
        business = args[0]
        number = args[1]
        if CheckWitness(TOKEN_OWNER):
            Log("Adding challenges to the business package.")
            return buy_challenge_package(ctx, business, number)
        else:
            return False

    if operation == 'create_challenge':
        owner = args[0]
        challenge_id = args[1]
        if CheckWitness(owner) and check(ctx, owner):
            Log("Creating challenge.")
            return create_challenge(ctx, owner, challenge_id)
        else:
            return False

    if operation == 'close_challenge':
        owner = args[0]
        challenge_id = args[1]
        if CheckWitness(args[0]) and check(ctx, owner):
            return close_challenge(ctx, owner, challenge_id)
        else:
            return False

    if operation == 'is_challenge_closed':
        owner = args[0]
        challenge_id = args[1]
        return is_challenge_closed(ctx, owner, challenge_id)
    
    if operation == 'is_challenge_open':
        owner = args[0]
        challenge_id = args[1]
        return is_challenge_open(ctx, owner, challenge_id)

    if operation == 'submission_number':
        owner = args[0]
        challenge_id = args[1]
        return submission_number(ctx, owner, challenge_id)

    if operation == 'challenge_expiry_date':
        owner = args[0]
        challenge_id = args[1]
        return challenge_expiry_date(ctx, owner, challenge_id)

    if operation == 'submit':
        if CheckWitness(args[0]):
            challenger = args[0]
            owner = args[1]
            challenge_id = args[2]
            Log("Creating submission.")
            status = create_submission(ctx, challenger, owner, challenge_id)
            return status
        else:
            return False

    if operation == 'submission_approver_number':
        challenger = args[0]
        owner = args[1]
        challenge_id = args[2]
        return submission_approver_number(ctx, challenger, owner, challenge_id)

    if operation == 'submission_rejecter_number':
        challenger = args[0]
        owner = args[1]
        challenge_id = args[2]
        return submission_rejecter_number(ctx, challenger, owner, challenge_id)

    if operation == 'submission_expiry_date':
        challenger = args[0]
        owner = args[1]
        challenge_id = args[2]
        return submission_expiry_date(ctx, challenger, owner, challenge_id)

    if operation == 'approve_submission':
        if CheckWitness(args[0]):
            voter = args[0]
            challenger = args[1]
            owner = args[2]
            challenge_id = args[3]
            Log("Approving submission.")
            status = approve(ctx, voter, challenger, owner, challenge_id)
            return status
        else:
            return False

    if operation == 'reject_submission':
        if CheckWitness(args[0]):
            voter = args[0]
            challenger = args[1]
            owner = args[2]
            challenge_id = args[3]
            Log("Rejecting submission.")
            status = reject(ctx, voter, challenger, owner, challenge_id)
            return status
        else:
            return False

    if operation == 'promoter_claim':
        if CheckWitness(args[0]):
            print("Claiming rewards for promoter.")
            challenger = args[0]
            owner = args[1]
            challenge_id = args[2]
            is_approved = promoter_fund_claim(ctx, challenger, owner, challenge_id)
            if is_approved:
                print("Promoter is approved for a claim.")
                amount = get_promoter_mining_rate(ctx)
                claim_funds(ctx, CHALLENGE_SYSTEM_RESERVE, challenger, amount)
                return True
            else:
                print("Promoter is not approved for a claim.")
                return False   
        else:
            return False

    if operation == 'approver_claim':
        if CheckWitness(args[0]):
            print("Claiming rewards for voter.")
            voter = args[0]
            challenger = args[1]
            owner = args[2]
            challenge_id = args[3]
            has_approved = approver_fund_claim(ctx, voter, challenger, owner, challenge_id)
            if has_approved != False:
                print("Voter is approved for a claim.")
                amount = get_approver_mining_rate(ctx, has_approved)
                claim_funds(ctx, CHALLENGE_SYSTEM_RESERVE, voter, amount)
                return True
            else:
                print("Voter is not approved for a claim.")
                return False    
        else:
            return False

    if operation == 'rejecter_claim':
        if CheckWitness(args[0]):
            print("Claiming rewards for voter.")
            voter = args[0]
            challenger = args[1]
            owner = args[2]
            challenge_id = args[3]
            has_rejected = rejecter_fund_claim(ctx, voter, challenger, owner, challenge_id)
            if has_rejected != False:
                print("Voter is approved for a claim.")
                amount = get_rejecter_mining_rate(ctx, has_rejected)
                claim_funds(ctx, CHALLENGE_SYSTEM_RESERVE, voter, amount)
                return True
            else:
                print("Voter is not approved for a claim.")
                return False 
        else:
            return False

    if operation == 'load_challenge_reserve':
        return load_challenge_reserve(ctx, args[0])

    return False

def claim_funds(ctx, t_from, t_to, amount):
    print("Claiming Funds.")
    print(amount)
    if amount <= 0:
        return False
    from_balance = Get(ctx, t_from)
    Log("Challenge Reserve Balance:")
    Log(from_balance)
    if from_balance < amount:
        print("Insufficient tokens in from balance. Contact Nodis.")
        return False
    to_balance = Get(ctx, t_to)
    new_from_balance = from_balance - amount
    new_to_balance = to_balance + amount
    Put(ctx, t_to, new_to_balance)
    Put(ctx, t_from, new_from_balance)
    OnTransfer(t_from, t_to, amount)
    print("Funds have been successfully claimed.")
    return True

def load_challenge_reserve(ctx, amount):
    if not CheckWitness(TOKEN_OWNER):
        print("Needs to be the token owner.")
        return False

    if amount <= 0:
        print("Negative amount.")
        return False

    owner_balance = Get(ctx, TOKEN_OWNER)
    if balance < amount:
        print("The owner does not have enough balance.")
        return False

    current_challenge_reserve = Get(ctx, CHALLENGE_SYSTEM_RESERVE)
    if current_challenge_reserve + amount > CHALLENGE_SYSTEM_INITIAL_AMOUNT:
        print("Funds would exceed the maximum amount for challenge reserve.")
        return False

    print("Adding funds to the challenge reserve.")

    new_balance = owner_balance - amount
    Put(ctx, TOKEN_OWNER, new_balance)

    new_challenge_reserve = current_challenge_reserve + amount
    Put(ctx, CHALLENGE_SYSTEM_RESERVE, new_challenge_reserve)

    return True