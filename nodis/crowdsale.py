from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Header import GetTimestamp
from boa.interop.Neo.Runtime import CheckWitness, GetTime
from boa.interop.Neo.Action import RegisterAction
from boa.interop.System.ExecutionEngine import GetScriptContainer
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from nodis.token import *
from nodis.txio import get_asset_attachments
from utils import valid_address

OnKYCRegister = RegisterAction('kyc_registration', 'address')
OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnRefund = RegisterAction('refund', 'addr_to', 'amount', 'asset') # V7

time = GetTime()

LAST_TX_KEY = b'LAST_TX_KEY'

def kyc_register(ctx, args):
    """

    :param args:list a list of addresses to register
    :param token:Token A token object with your ICO settings
    :return:
        int: The number of addresses to register for KYC
    """
    ok_count = 0

    if CheckWitness(TOKEN_OWNER):

        for address in args:

            if len(address) == 20:

                kyc_storage_key = concat(KYC_KEY, address)
                Put(ctx, kyc_storage_key, True)

                OnKYCRegister(address)
                ok_count += 1

    return ok_count


def kyc_status(ctx, args):
    """
    Gets the KYC Status of an address

    :param args:list a list of arguments
    :return:
        bool: Returns the kyc status of an address
    """

    if len(args) > 0:
        addr = args[0]
        #V8
        if not valid_address(addr):
            return False
        kyc_storage_key = concat(KYC_KEY, addr)

        return Get(ctx, kyc_storage_key)

    return False


def perform_exchange(ctx):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """

    # V2
    last_tx = Get(ctx, LAST_TX_KEY)
    current_tx = GetScriptContainer().Hash
    if last_tx == current_tx:
        return False
    Put(ctx, LAST_TX_KEY, current_tx)

    attachments = get_asset_attachments()  # [receiver, sender, neo, gas]

    # this looks up whether the exchange can proceed
    exchange_ok = can_exchange(ctx, attachments)

    if not exchange_ok:
        print("You cannot exchange! Contact Nodis for refunds!")
        #V7
        if attachments[2] > 0:
            OnRefund(attachments[1], attachments[2], 'neo')
        if attachments[3] > 0:
            OnRefund(attachments[1], attachments[3], 'gas')
        return False

    print("We will proceed with the exchange of tokens now.")

    # lookup the current balance of the address
    current_balance = Get(ctx, attachments[1])

    exchanged_tokens = attachments[3] * TOKENS_PER_GAS_SERIES_A / 100000000

    # add it to the exchanged tokens and persist in storage
    new_total = exchanged_tokens + current_balance
    Put(ctx, attachments[1], new_total)

    # update the in circulation amount
    result = add_to_circulation(ctx, exchanged_tokens)

    # dispatch transfer event
    OnTransfer(attachments[0], attachments[1], exchanged_tokens)

    return True

#V21
def can_exchange(ctx, attachments):
    """
    Determines if the contract invocation meets all requirements for the ICO exchange
    of neo or gas into NEP5 Tokens.
    Note: This method can be called via both the Verification portion of an SC or the Application portion

    When called in the Verification portion of an SC, it can be used to reject TX that do not qualify
    for exchange, thereby reducing the need for manual NEO or GAS refunds considerably

    :param attachments:Attachments An attachments object with information about attached NEO/Gas assets
    :return:
        bool: Whether an invocation meets requirements for exchange
    """
    #V7
    if attachments[2] > 0:
        print("NEO not accepted!")
        return False

    # If you have less than 50 GAS, the minting will be refused.
    if attachments[3] < 50 * 100000000:
        print("Not enough gas attached!")
        return False

    # the following looks up whether an address has been
    # registered with the contract for KYC regulations
    # this is not required for operation of the contract
    #V4, V8
    if not valid_address(attachments[1]):
        return False

    if not get_kyc_status(ctx, attachments[1]):
        print("You have not been registered for the Token sale.")
        return False

    print("You are registered for the Token sale.")
    
    # calculate the amount requested
    amount_requested = attachments[3] * TOKENS_PER_GAS_SERIES_A / 100000000

    exchange_ok = calculate_can_exchange(ctx, amount_requested)

    return exchange_ok


def get_kyc_status(ctx, address):
    """
    Looks up the KYC status of an address

    :param address:bytearray The address to lookup
    :param storage:StorageAPI A StorageAPI object for storage interaction
    :return:
        bool: KYC Status of address
    """
    # V8
    if not valid_address(address):
        return False

    kyc_storage_key = concat(KYC_KEY, address)

    return Get(ctx, kyc_storage_key)

#V21
def calculate_can_exchange(ctx, amount):
    """
    Perform custom token exchange calculations here.

    :param amount:int Number of tokens to convert from asset to tokens
    :return:
        bool: Whether or not an address can exchange a specified amount
    """

    if time < SERIES_A_START:
        print("Series A has not started!")
        return False

    if time > SERIES_A_END:
        print("Series A is over! Please contact Nodis for private sales.")
        return False

    # check amount available for Series A
    amount_available = crowdsale_available_amount(ctx)

    if amount > amount_available:
        print("Not enough tokens available for Series A!")
        return False

    else:
        print("Tokens available for Series A!")
        return True

    return False
