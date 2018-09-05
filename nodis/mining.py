from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash, GetCallingScriptHash
from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat


from nodis.token import *
from nodis.nep5 import do_transfer_from
from nodis.challenge.challenge import create_challenge, submit, close_challenge
from nodis.submission.submission import create_submission, approve, reject, promoter_fund_claim, rejecter_fund_claim, approver_fund_claim


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
    Delete(ctx, address)
    return True

def handle_mining(ctx, operation, args):

    if operation == 'register_business':
        address = args[0]
        if CheckWitness(TOKEN_OWNER):
            status = register(ctx, address)
            return status

    if operation == 'check_business':
        address = args[0]
        status = check(ctx, address)
        return status

    if operation == 'signout_business':
        address = args[0]
        if CheckWitness(TOKEN_OWNER):
            status = signout(ctx, address)
            return status

    if operation == 'create_challenge':
        owner = args[0]
        challenge_id = args[1]
        if CheckWitness(owner) and check(ctx, owner):
            return create_challenge(ctx, owner, challenge_id)
        return False

    if operation == 'close_challenge':
        owner = args[0]
        challenge_id = args[1]
        if CheckWitness(args[0]) and check(ctx, owner):
            return close_challenge(ctx, owner, challenge_id)
        return False

    if operation == 'submit':
        if CheckWitness(args[0]):
            challenger = args[0]
            owner = args[1]
            challenge_id = args[2]
            status = create_submission(ctx, challenger, owner, challenge_id)
            return status

    if operation == 'approve':
        if CheckWitness(args[0]):
            voter = args[0]
            challenger = args[1]
            owner = args[2]
            challenge_id = args[3]
            status = approve(ctx, challenger, owner, challenge_id)
            return status

    if operation == 'reject':
        if CheckWitness(args[0]):
            voter = args[0]
            challenger = args[1]
            owner = args[2]
            challenge_id = args[3]
            status = reject(ctx, challenger, owner, challenge_id)
            return status

    if operation == 'promoter_claim':
        if CheckWitness(args[0]):
            challenger = args[0]
            owner = args[1]
            challenge_id = args[2]
            is_approved = promoter_fund_claim(ctx, challenger, owner, challenge_id)
            if is_approved:
                fund = get_promoter_mining_rate(ctx)
                do_transfer_from(ctx, TOKEN_OWNER, owner, fund)
                return True

    if operation == 'approver_claim':
        if CheckWitness(args[0]):
            voter = args[0]
            challenger = args[1]
            owner = args[2]
            challenge_id = args[3]
            has_approved = approver_fund_claim(ctx, voter, challenger, owner, challenge_id)
            if has_approved:
                fund = get_approver_mining_rate(ctx)
                do_transfer_from(ctx, TOKEN_OWNER, owner, fund)
                return True

    if operation == 'rejecter_claim':
        if CheckWitness(args[0]):
            voter = args[0]
            challenger = args[1]
            owner = args[2]
            challenge_id = args[3]
            has_rejected = rejecter_fund_claim(ctx, voter, challenger, owner, challenge_id)
            if has_rejected:
                fund = get_rejecter_mining_rate(ctx)
                do_transfer_from(ctx, TOKEN_OWNER, owner, fund)
                return True