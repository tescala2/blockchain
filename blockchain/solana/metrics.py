import pandas as pd
from requests import post
from datetime import datetime as dt
import pytz


def metrics_df(rpc):
    def helper(payload, rpc):
        r = post(rpc, json=payload)
        j = r.json()

        return j

    def get_supply(rpc):
        payload = {
            "jsonrpc":"2.0",
            "id":1,
            "method":"getSupply"
        }

        j = helper(payload, rpc)

        circ_supply = j['result']['value']['circulating']/10**9
        ncirc_supply = j['result']['value']['nonCirculating']/10**9

        return circ_supply, ncirc_supply, circ_supply/(circ_supply+ncirc_supply)

    def get_tps(rpc, tf=10):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getRecentPerformanceSamples",
            "params": [tf]
        }

        j = helper(payload, rpc)

        tps_list = []
        for result in j['result']:
            tps = result['numTransactions']/result['samplePeriodSecs']
            slot = result['slot']
            tps_list.append(tps)

        return round(sum(tps_list)/len(tps_list))

    def get_epoch_info(rpc):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getEpochInfo"
        }

        j = helper(payload, rpc)

        return j['result']['absoluteSlot'], j['result']['blockHeight'], j['result']['epoch'], j['result']['transactionCount']


    tps = get_tps(rpc)
    slot, block_height, epoch, tx_count = get_epoch_info(rpc)
    circ_supply, ncirc_supply, circ_ratio = get_supply(rpc)
    data_list = [tps, slot, block_height, epoch, tx_count, circ_supply, ncirc_supply, circ_ratio]
    col_list = ['TPS', 'Slot', 'Block Height', 'Epoch', 'TX Count', 'Circulating Supply', 'Non-Circulating Supply', 'Percent in Circulation']

    df = pd.DataFrame.from_dict(data={dt.now(tz=pytz.timezone('UTC')):data_list},
                                orient='index',
                                columns=col_list)

    return df


rpc_main = 'https://api.mainnet-beta.solana.com'

print(metrics_df(rpc_main))


