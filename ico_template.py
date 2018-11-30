"""
NEX ICO Template
===================================

Author: Thomas Saunders
Email: tom@neonexchange.org

Date: Dec 11 2017

"""
from nodis.txio import get_asset_attachments
from nodis.token import *
from nodis.crowdsale import *
from nodis.nep5 import *
from nodis.mining import handle_mining
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness, Log, Notify
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import *

ctx = GetContext()
NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']
MINING_METHODS = ['register_business', 'check_business', 'signout_business', 'create_challenge', 'close_challenge', 'submit', 'approve_submission', 'reject_submission', 'promoter_claim', 'approver_claim', 'rejecter_claim', 'get_mining_rate', 'get_promoter_mining_rate', 'get_approver_mining_rate', 'get_rejecter_mining_rate', 'claim_referral_fee', 'check_challenge_package', 'buy_challenge_package']


def Main(operation, args):
    """

    :param operation: str The name of the operation to perform
    :param args: list A list of arguments along with the operation
    :return:
        bytearray: The result of the operation
    """

    trigger = GetTrigger()

    # This is used in the Verification portion of the contract
    # To determine whether a transfer of system assets ( NEO/Gas) involving
    # This contract's address can proceed
    if trigger == Verification():

        # check if the invoker is the owner of this contract
        is_owner = CheckWitness(TOKEN_OWNER)

        # If owner, proceed
        if is_owner:

            return True

        # Otherwise, we need to lookup the assets and determine
        # If attachments of assets is ok
        attachments = get_asset_attachments()
        return can_exchange(ctx, attachments, True)

    elif trigger == Application():

        for op in NEP5_METHODS:
            if operation == op:
                return handle_nep51(ctx, operation, args)

        for op in MINING_METHODS:
            if operation == op:
                return handle_mining(ctx, operation, args)
        
        if operation == 'deploy':
            return deploy()

        elif operation == 'circulation':
            return get_circulation(ctx)

        # the following are handled by crowdsale

        elif operation == 'mintTokens':
            return perform_exchange(ctx)

        elif operation == 'crowdsale_register':
            return kyc_register(ctx, args)

        elif operation == 'crowdsale_status':
            return kyc_status(ctx, args)

        elif operation == 'crowdsale_available':
            return crowdsale_available_amount(ctx)

        elif operation == 'get_attachments':
            return get_asset_attachments()

        return 'unknown operation'

    return False


def deploy():
    """

    :param token: Token The token to deploy
    :return:
        bool: Whether the operation was successful
    """
    if not CheckWitness(TOKEN_OWNER):
        print("Must be owner to deploy")
        return False

    if not Get(ctx, 'initialized'):
        # do deploy logic
        Put(ctx, 'initialized', 1)
        Put(ctx, TOKEN_OWNER, TOKEN_OWNER_AMOUNT)
        Put(ctx, CHALLENGE_SYSTEM_RESERVE, CHALLENGE_SYSTEM_INITIAL_AMOUNT)
        circulation = TOKEN_OWNER_AMOUNT + CHALLENGE_SYSTEM_INITIAL_AMOUNT
        Log("Deployed successfully!")
        return add_to_circulation(ctx, circulation)

    return False
