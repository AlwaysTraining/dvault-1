import itertools
from dvault.strats import (Dvine, Dmoon)
from dvault.accounts import (Alpaca,get_alpaca_args)


class dvine_us_equity:
    strat = Dvine
    entry_point_base = ["dvine"] + strat.default_args + [
            '--log-level', 'INFO',
            '--strategy-bet-size-usd', 100 ]


_DVINE_DAY_ARG_NAMES = [
        ( 1,200,50     ),
        ( 2,213,53     ),
        ( 3,220,55     ),
        ( 4,227,57     ),
        ( 5,233,58     ),
        ( 6,240,60     ),
        ( 7,247,62     ),
        ( 8,253,63     ),
        ( 9,260,65     ),
        ( 10,267,67    ),
        ( 11,273,68    ),
        ( 12,280,70    ),
        ( 13,286,71    ),
        ( 14,293,73    ),
        ( 15,300,75    ),
        ( 16,307,77    ),
        ( 17,313,78    ),
        ( 18,320,80    ),
        ( 19,327,82    ),
        ( 20,333,83    ),
        ( 21,340,85    ),
        ( 22,347,87    ),
        ( 23,353,88    ),
        ( 24,360,90    ),
        ( 25,367,92    ),
        ( 26,373,93    ),
        ( 27,380,95    ),
        ( 28,387,97    ),
        ( 29,393,98    ),
        ( 30,400,100   ),
        ( 33,419,104   ),
        ( 36,439,109   ),
        ( 39,459,114   ),
        ( 43,486,121   ),
        ( 47,513,128   ),
        ( 52,546,136   ),
        ( 57,579,144   ),
        ( 63,619,154   ),
        ( 69,659,164   ),
        ( 76,705,175   ),
        ( 84,759,189   ),
        ( 93,818,203   ),
        ( 100,900,300  ),
        ( 150,1350,450 ),
        ( 200,1800,600 ),
        ( 253,2277,759 ) ]

_VARIATION_ARG_NAMES = [
        '--trade-days-per-bar',
        '--objective-num-trade-days',
        '--threshold-num-trade-days' ]

# For some rason inside generator expressions you can't access your own class
# variables, so I have moved a lot of things out to the global namespace
#
# don't feel bad if you can't read the code below, it is write only.
# basically it is doing a mail merge cross multiply of the arg names with the
# day tuples to build a list of lists of cmd line arguments
_DVINE_DAYS = [
        list(itertools.chain.from_iterable(
            [ [arg_name, _DVINE_DAY_ARG_NAMES[i][j] ] for j, arg_name in enumerate(_VARIATION_ARG_NAMES) ]
            ))
        for i in range(len(_DVINE_DAY_ARG_NAMES))
        ]

def _get_purge_args(purge_base, postfix_args=[]):

    purge_orders_cmd = purge_base + [
            '--purge-type', 'orders', '--log-level', 'INFO']
    purge_positions_cmd = purge_base + [
            '--purge-type', 'positions', '--log-level', 'INFO']
    purge_sleep = ['sleep','2m']
    purge_cmds = [
            purge_orders_cmd + postfix_args,
            purge_sleep,
            purge_positions_cmd + postfix_args,
            purge_sleep,
            purge_positions_cmd + postfix_args ]
    return purge_cmds


class dvine_us_equity_3Pct(dvine_us_equity):
    account = Alpaca.dvine_us_equity_3Pct
    alpaca_args = get_alpaca_args(account)
    entry_point_base = dvine_us_equity.entry_point_base + alpaca_args + [
            '--nstd-thresh', 0.03 ]
    first_base = entry_point_base
    rest_base = entry_point_base + [
            '--bar-shift-multiplier', -1,
            '--bar-shift-multiplier', 0,
            '--clear-persistence' ]
    compute_orders_cmds = None # Complicated initialization done below, outside the class
    purge_base = ['dvine_purge'] + dvine_us_equity.strat.base_args + alpaca_args
    purge_cmds = _get_purge_args(purge_base)


# The first command runs daily in the traditional sense with persistence
# The rest of the commands clear persistence, and then seed themselves with a
# -1 shft, and then run at now time.  Really we should write a new version of
# dvine that does this by default, so we don't have the workaround of the two
# --bar-shift-multiplier's
dvine_us_equity_3Pct.compute_orders_cmds = [
        dvine_us_equity_3Pct.first_base + _DVINE_DAYS[0]] + [
        dvine_us_equity_3Pct.rest_base  +  x for x in _DVINE_DAYS[1:36] ]


class dvine_us_equity_2Pct(dvine_us_equity):
    account = Alpaca.dvine_us_equity_2Pct
    alpaca_args = get_alpaca_args(account)
    entry_point_base = dvine_us_equity.entry_point_base + alpaca_args + [
            '--nstd-thresh', 0.0249,
            '--strategy-bet-size-usd', 500.00]
    rest_base = entry_point_base + [
            '--bar-shift-multiplier', -1,
            '--bar-shift-multiplier', 0,
            '--clear-persistence' ]
    compute_orders_cmds = None # Complicated initialization done below, outside the class
    purge_base = ['dvine_purge'] + dvine_us_equity.strat.base_args + alpaca_args
    purge_cmds = _get_purge_args(purge_base)


dvine_us_equity_2Pct.compute_orders_cmds = [
        dvine_us_equity_2Pct.rest_base  +  x for x in _DVINE_DAYS[14:30] ]

class dvine_us_equity_5Pct(dvine_us_equity):
    account = Alpaca.dvine_us_equity_5Pct
    alpaca_args = get_alpaca_args(account)
    entry_point_base = dvine_us_equity.entry_point_base + alpaca_args + [
            '--nstd-thresh', 0.05,
            '--strategy-bet-size-usd', 100.00]
    rest_base = entry_point_base + [
            '--bar-shift-multiplier', -1,
            '--bar-shift-multiplier', 0,
            '--clear-persistence' ]
    compute_orders_cmds = None # Complicated initialization done below, outside the class
    purge_base = ['dvine_purge'] + dvine_us_equity.strat.base_args + alpaca_args
    purge_cmds = _get_purge_args(purge_base)


dvine_us_equity_5Pct.compute_orders_cmds = [
        dvine_us_equity_5Pct.rest_base  +  x for x in _DVINE_DAYS[31:] ]



class dmoon:
    strat = Dmoon
    entry_point_base = ["dmoon"] + strat.default_args + []

class dmoon_adhoc(dmoon):
    discord_webhook_url = "https://discord.com/api/webhooks/985008285914636288/SoT91_xorPb7-Ch4FsQEDhmXkXz2yht9C8lqmcuw0vlR-FrGEiNP3gXXYE78c4tpyZdz" # to general channel on dvine server

    common_args = ['--universe-name', 'crypto']
    entry_point_base = dmoon.entry_point_base + common_args + [
            '--discord-webhook-url', discord_webhook_url]

    entry_point = entry_point_base

class dmoon_adhoc_3s(dmoon_adhoc):
    account = Alpaca.play_time
    alpaca_args = get_alpaca_args(account)
    entry_point = dmoon_adhoc.entry_point_base + alpaca_args + [
            '--period-span-value', 10.0,
            '--period-span-units', 'Sec',
            '--bot-name', 'dmoon_adhoc_3s',
            '--strategy-bet-size-usd', 50000,
            '--entry-signal-look-back-periods', 3,
            '--exit-signal-look-back-periods', 2 ]


class dmoon_adhoc_dev(dmoon_adhoc):
    account = Alpaca.play_time
    alpaca_args = get_alpaca_args(account)
    entry_point = dmoon_adhoc.entry_point_base + alpaca_args + [
            '--period-span-value', 1,
            '--period-span-units', 'Min',
            '--bot-name', 'dmoon_adhoc_dev',
            '--strategy-bet-size-usd', 50000,
            '--entry-signal-look-back-periods', 6, #10
            '--exit-signal-look-back-periods', 4 ] #6


class dmoon_adhoc_5m(dmoon_adhoc):
    account = Alpaca.play_time
    alpaca_args = get_alpaca_args(account)
    entry_point = dmoon_adhoc.entry_point_base +  alpaca_args +[
            '--period-span-value', 5,
            '--period-span-units', 'Min',
            '--bot-name', 'dmoon_adhoc_5m',
            '--strategy-bet-size-usd', 50000,
            '--entry-signal-look-back-periods', 7,
            '--exit-signal-look-back-periods', 3 ]

class dmoon_adhoc_1m(dmoon_adhoc):
    account = Alpaca.dmoon_alpha
    alpaca_args = get_alpaca_args(account)
    entry_point = dmoon_adhoc.entry_point_base +  alpaca_args +[
            '--period-span-value', 1,
            '--period-span-units', 'Min',
            '--bot-name', 'dmoon_adhoc_1m',
            '--strategy-bet-size-usd', 50000,
            '--entry-signal-look-back-periods', 2,
            '--exit-signal-look-back-periods', 2 ]
