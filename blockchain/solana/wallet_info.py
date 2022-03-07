from requests import post
import pandas as pd


def wallet_info_df(rpc, wallets):
    def helper(payload, rpc=rpc):
        r = post(rpc, json=payload)
        return r.json()

    def get_balance(wallet):
        payload = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'getBalance',
            'params': [
                f'{wallet}'
            ]
        }

        j = helper(payload)

        return j['result']['value'] / 10 ** 9

    def get_token_balances(wallet):
        payload = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'getTokenAccountsByOwner',
            'params': [
                f'{wallet}',
                {
                    'programId': 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
                },
                {
                    'encoding': 'jsonParsed'
                }
            ]
        }

        j = helper(payload)

        balances = []
        for value in j['result']['value']:
            amt = value['account']['data']['parsed']['info']['tokenAmount']['uiAmount']
            key = value['pubkey']
            if amt < 1:
                continue
            else:
                balances.append([key, amt])

        return balances

    def get_txs(wallet):
        payload = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'getSignaturesForAddress',
            'params': [
                f'{wallet}',
                {
                    'limit': 5
                }
            ]
        }

        j = helper(payload)

        tx_sigs = []
        for result in j['result']:
            tx_sigs.append(result['signature'])

        return tx_sigs

    wallet_dict = {}
    for wallet in wallets:
        wallet_dict[wallet] = [get_balance(wallet), get_txs(wallet), get_token_balances(wallet)]

    return pd.DataFrame.from_dict(wallet_dict,
                                  orient='index',
                                  columns=['sol balance', 'tx history', 'token balances'])


rpc_main = 'https://api.mainnet-beta.solana.com'
# rpc_dev = 'https://api.devnet.solana.com'

# substitute this list with your list of wallets
wallets = ['DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK', '7S3P4HxJpyyigGzodYwHtCxZyUQe9JiBMHyRWXArAaKv']

print(wallet_info_df(rpc_main, wallets))
