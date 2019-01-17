"""
Basic settings for an NEP5 Token and crowdsale
"""

from boa.interop.Neo.Storage import *
from boa.interop.Neo.Runtime import CheckWitness, Notify, Log

TOKEN_NAME = 'Nodis Token'

TOKEN_SYMBOL = 'NODIS'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
TOKEN_OWNER = b'\x9e\x9a\\\xfd\xb5\x18\xb83\x89e\xf4\x94\xb2\x15u\x0eh\xc2,\xa7'

# Address of the challenge reserve
CHALLENGE_SYSTEM_RESERVE = b'CHALLENGE_SYSTEM_RESERVE'

TOKEN_CIRC_KEY = b'in_circulation'

TOKEN_TOTAL_SUPPLY = 100000000 * 100000000  # 100m total supply * 10^8 ( decimals)

TOKEN_OWNER_AMOUNT = 25200000 * 100000000  # 25m owners + 200k airdrop

CHALLENGE_SYSTEM_INITIAL_AMOUNT = 55000000 * 100000000 # 55m to the Challenge Reserve.

SERIES_B_TOTAL_AMOUNT = 15800000 * 100000000 # total amount available to during Series B

INITIAL_MINING_RATE = 50 * 100000000 # Initial mining rate upon deployment.

# Token Gas conversion rate for Series A
TOKENS_PER_GAS_SERIES_A = 905000000

# Token Gas conversion rate for Series B
TOKENS_PER_GAS_SERIES_B = 769000000

# Series A Token Sale Start Date (Sat, 06 Apr 2019 00:00 AM)
SERIES_A_START = 1554526800

# Series A Token Sale End Date (Thu, 06 Jun 2019 00:00 AM)
SERIES_A_END = 1559797200

# Series B Token Sale Start Date (Sat, 05 Oct 2019 00:00 AM)
SERIES_B_START = 1570251600

# Series B Token Sale End Date (Thu, 05 Dec 2019 00:00 AM)
SERIES_B_END = 1575522000

KYC_KEY = b'kyc_ok'

SERIES_A_KEY = b'r1'
    

def crowdsale_available_amount(ctx):
    """
    Return the amount of tokens available to the crowdsale.

    :return: int The amount of tokens left for sale in the crowdsale
    """

    in_circ = Get(ctx, TOKEN_CIRC_KEY)

    available = TOKEN_TOTAL_SUPPLY - in_circ

    return available


def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circulation

    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, TOKEN_CIRC_KEY)

    current_supply += amount

    Put(ctx, TOKEN_CIRC_KEY, current_supply)

    return True


def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation

    :return:
        int: Total amount in circulation
    """
    return Get(ctx, TOKEN_CIRC_KEY)


def get_mining_rate(ctx):
    """
    Get the current mining rate. The mining rate is 50 Nodis upon deployment. The mining rate can be calculated by the following formula:

    mining rate = initial mining rate * (current challenge reserve / initial challenge reserve)

    :return:
        int: Current mining rate
    """
    # Needs to be tested more thoroughly especially when the supply increases.

    current_reserve = Get(ctx, CHALLENGE_SYSTEM_RESERVE)

    if current_reserve != 0:

        current_inverse_rate = CHALLENGE_SYSTEM_INITIAL_AMOUNT / current_reserve

        return INITIAL_MINING_RATE / current_inverse_rate

    else:

        return 0


def get_promoter_mining_rate(ctx):
    """
    Get the mining rate for successful promoters. A promoter gets 80% of the mining rate.

    :return:
        int: Mining rate for successful promoters.
    """

    mining_rate = get_mining_rate(ctx)

    rate = mining_rate / 10

    return rate * 80


def get_rejecter_mining_rate(ctx, number_of_rejecters):
    """
    Get the mining rate for successful rejecters. Successful rejecters share 8% of the mining rate.

    :return:
        int: The mining rate for successful rejecters divided by the number of rejecters.
    """

    mining_rate = get_mining_rate(ctx)

    rate = mining_rate / 100

    rejecters_reward = 8 * rate

    return rejecters_reward / number_of_rejecters
    

def get_approver_mining_rate(ctx, number_of_approvers):
    """
    Get the mining rate for successful approvers. Successful approvers share 12% of the mining rate.

    :return:
        int: The mining rate for successful approvers divided by the number of approvers. 
    """

    mining_rate = get_mining_rate(ctx)

    rate = mining_rate / 100

    approvers_reward = 12 * rate

    return approvers_reward / number_of_approvers