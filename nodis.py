"""
NODIS Token Smart Contract
===================================

Authors: Nathan Mukena & Dominic Fung
Emails: nathan.mukena@nodis.io & dominic.fung@nodis.io

Date: March 15 2019

"""
from nodis.txio import get_asset_attachments
from nodis.token import *
from nodis.crowdsale import *
from nodis.nep5 import *
from nodis.mining import handle_mining
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness, Log, Notify, GetTime
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import *
from boa.interop.Neo.Blockchain import Migrate, Destroy, GetAccount
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from boa.interop.Neo.Account import GetBalance

ctx = GetContext()
NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']
MINING_METHODS = ['register_business', 'check_business', 'signout_business', 'create_challenge', 'close_challenge', 'submit', 'approve_submission', 'reject_submission', 'promoter_claim', 'approver_claim', 'rejecter_claim', 'get_mining_rate', 'get_promoter_mining_rate', 'get_approver_mining_rate', 'get_rejecter_mining_rate', 'check_challenge_package', 'buy_challenge_package', 'challenge_reserve', 'load_challenge_reserve', 'is_challenge_closed', 'is_challenge_open', 'submission_number', 'challenge_expiry_date', 'submission_approver_number', 'submission_rejecter_number', 'submission_expiry_date']

NEO = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'
GAS = b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`'

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
        # V10
        is_owner = CheckWitness(get_owner_address(ctx))

        # If owner, proceed
        if is_owner:
            return True

        # Otherwise, we need to lookup the assets and determine
        # If attachments of assets is ok
        attachments = get_asset_attachments()

        #V1
        if attachments[4]:
            return False

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

        elif operation == 'reallocate':
            return reallocate()

        elif operation == 'get_attachments':
            return get_asset_attachments()

        #V17
        elif operation == 'supportedStandards':
            return ['NEP-5', 'NEP-10']

        elif operation == 'migrate':
            #V11
            if len(args) != 9:
                return False
            if not CheckWitness(get_owner_address(ctx)):
                return False
            account = GetAccount(GetExecutingScriptHash())
            neo_balance = GetBalance(account, NEO)
            gas_balance = GetBalance(account, GAS)
            if neo_balance > 0:
                print("Cannot migrate yet.  Please transfer all neo/gas and tokens from contract address")
                return False
            if gas_balance > 0:
                print("Cannot migrate yet.  Please transfer all neo/gas and tokens from contract address")
                return False
            Migrate(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8])
            return True

        elif operation == 'destroy':
            #V11
            if not CheckWitness(get_owner_address(ctx)):   
                return False
            account = GetAccount(GetExecutingScriptHash())
            neo_balance = GetBalance(account, NEO)
            gas_balance = GetBalance(account, GAS)
            if neo_balance > 0:
                print("Cannot migrate yet.  Please transfer all neo/gas and tokens from contract address")
                return False
            if gas_balance > 0:
                print("Cannot migrate yet.  Please transfer all neo/gas and tokens from contract address")
                return False
            Destroy()
            return True
        
        #V10
        elif operation == 'change_owner':
            #V10
            if not CheckWitness(get_owner_address(ctx)):   
                return False
            #V11
            if len(args) != 1:
                return False
            # V13
            if not valid_address(args[0]):
                return False
            new_address = args[0]
            return set_owner_address(ctx, new_address)

        return 'unknown operation'

    return False


def deploy():
    """

    :return:
        bool: Whether the operation was successful
    """
    #V10
    owner_initial_address = b'\xcca\xe4\xaa\x9eS\x13.\xb1o\x10}\xf6|\x01\x06\x1f\x8b\xa2K'
    set_owner_address(ctx, owner_initial_address)

    if not CheckWitness(get_owner_address(ctx)):
        print("Must be owner to deploy")
        return False

    if not Get(ctx, 'initialized'):
        # do deploy logic
        Put(ctx, 'initialized', 1)

        # Allocate owner balance of 41 m
        Put(ctx, get_owner_address(ctx), TOKEN_OWNER_AMOUNT)

        # Allocate Challenge Reserve balance
        Put(ctx, CHALLENGE_SYSTEM_RESERVE, CHALLENGE_SYSTEM_INITIAL_AMOUNT)
        
        circulation = TOKEN_OWNER_AMOUNT + CHALLENGE_SYSTEM_INITIAL_AMOUNT

        Log("Deployed successfully!")

        # Add owner balance and challenge reserve balance to circulation
        return add_to_circulation(ctx, circulation)

    return False

def reallocate():
    """
    
    Once the token sale is over, the owner can take back the remaining tokens.
    :return:
        bool: Whether the operation was successful
    """
    if not CheckWitness(get_owner_address(ctx)):
        print("Must be owner to reallocate")
        return False

    time = GetTime()

    if time < SERIES_A_END:
        print("Must wait until the end of Series A before re-allocating.")
        return False

    current_balance = Get(ctx, get_owner_address(ctx))

    crowdsale_available = crowdsale_available_amount(ctx)

    new_balance = current_balance + crowdsale_available

    Put(ctx, get_owner_address(ctx), new_balance)

    Log("Reallocated successfully!")

    # V14
    return add_to_circulation(ctx, crowdsale_available)