"""
Basic settings for an NEP5 Token and crowdsale
"""

from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import CheckWitness, Notify, Log

TOKEN_NAME = 'Nodis Token'

TOKEN_SYMBOL = 'NODIS'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the walet open, use ``wallet`` command
TOKEN_OWNER = b'\x9e\x9a\\\xfd\xb5\x18\xb83\x89e\xf4\x94\xb2\x15u\x0eh\xc2,\xa7'

CHALLENGE_SYSTEM_RESERVE = b'CHALLENGE_SYSTEM_RESERVE'

TOKEN_CIRC_KEY = b'in_circulation'

TOKEN_TOTAL_SUPPLY = 100000000 * 100000000  # 100m total supply * 10^8 ( decimals)

TOKEN_OWNER_AMOUNT = 40000000 * 100000000  # 40m to owners * 10^8

CHALLENGE_SYSTEM_INITIAL_AMOUNT = 55000000 * 100000000 # 55m to the Challenge System.

# for now assume 1 dollar per token, and one neo = 40 dollars * 10^8
TOKENS_PER_NEO = 40 * 100000000

# for now assume 1 dollar per token, and one gas = 20 dollars * 10^8
TOKENS_PER_GAS = 20 * 100000000

# maximum amount you can mint in the limited round ( 500 neo/person * 40 Tokens/NEO * 10^8 )
MAX_EXCHANGE_LIMITED_ROUND = 500 * 40 * 100000000

# when to start the crowdsale
BLOCK_SALE_START = 0

# when to end the initial limited round
LIMITED_ROUND_END = 0

KYC_KEY = b'kyc_ok'

LIMITED_ROUND_KEY = b'r1'
    

def crowdsale_available_amount(ctx):
    """

    :return: int The amount of tokens left for sale in the crowdsale
    """

    in_circ = Get(ctx, TOKEN_CIRC_KEY)

    available = TOKEN_TOTAL_SUPPLY - in_circ

    return available


def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation

    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, TOKEN_CIRC_KEY)

    current_supply += amount

    Put(ctx, TOKEN_CIRC_KEY, current_supply)

    return True

def allocate_to_challenge(ctx, owner, challenge_id, balance):
    """
    Allocate Nodis to challenges.
    """
    add_to_circulation(ctx, balance)
    return balance

def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation

    :return:
        int: Total amount in circulation
    """
    return Get(ctx, TOKEN_CIRC_KEY)


def get_mining_rate(ctx):
    """
    Get the current mining rate.

    :return:
        int: Current mining rate
    """
    initial_mining_rate = 50 * 100000000

    current_reserve = Get(ctx, CHALLENGE_SYSTEM_RESERVE)

    if current_reserve != 0:

        current_inverse_rate = CHALLENGE_SYSTEM_INITIAL_AMOUNT / current_reserve

        return initial_mining_rate / current_inverse_rate

    else:

        return 0


def get_promoter_mining_rate(ctx):
    """
    Get the current mining rate.

    :return:
        int: Mining rate for successful promoters (90% of the current mining rate)
    """

    mining_rate = get_mining_rate(ctx)

    rate = mining_rate/10

    return rate * 80

def get_rejecter_mining_rate(ctx, number_of_rejecters):
    """
    Get the current mining rate for successful rejecters.

    :return:
        int: Mining rate for successful rejecters (90% of the current mining rate)
    """

    mining_rate = get_mining_rate(ctx)

    rate = mining_rate/100

    rejecters_reward = 8 * rate

    return rejecters_reward / number_of_rejecters

def get_approver_mining_rate(ctx, number_of_approvers):
    """
    Get the current mining rate.

    :return:
        int: Current mining rate
    """

    mining_rate = get_mining_rate(ctx)

    rate = mining_rate/100

    approvers_reward = 12 * rate

    return approvers_reward / number_of_approvers

def get_referral_mining_rate(ctx):
    """
    Get the current mining rate.

    :return:
        int: Current mining rate
    """

    mining_rate = get_mining_rate(ctx)

    rate = mining_rate/100

    referral_rate = 60 * rate

    return referral_rate
