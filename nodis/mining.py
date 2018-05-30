from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat

from nodis.token import *
from nodis.challenge.challenge import *

OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve', 'addr_from', 'addr_to', 'amount')

def handle_mining(ctx, operation, args):

    if operation == 'create_challenge':
        return create_challenge(ctx, args[0], args[1])

    if operation == 'open_challenge':
        mine_rate = get_mine_rate(ctx)
        balance = mine_rate * 50
        allocate_to_challenge(ctx, args[0], args[1], balance)
        return open_challenge(ctx, args[0], args[1], balance)

    if operation == 'close_challenge':
        return close_challenge(ctx, args[0], args[1])
