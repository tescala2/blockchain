import pandas as pd
from datetime import date

current_date = date.today()

df = pd.read_csv('uniswapTokens_2022-05-03.csv')

stable = ['USDC', 'USDT', 'DAI', 'FEI', 'UST']
not_stable = ['WETH', 'LOOKS', 'APE']

stable_tvl = 0
stable_txcount = 0
stable_vol = 0
stable_fees = 0
not_stable_tvl = 0
not_stable_txcount = 0
not_stable_vol = 0
not_stable_fees = 0

for token in stable:
    stable_tvl += float(df[df['symbol'] == token]['totalValueLockedUSD'])
    stable_txcount += float(df[df['symbol'] == token]['txCount'])
    stable_vol += float(df[df['symbol'] == token]['volumeUSD'])
    stable_fees += float(df[df['symbol'] == token]['feesUSD'])

for token in not_stable:
    not_stable_tvl += float(df[df['symbol'] == token]['totalValueLockedUSD'])
    not_stable_txcount += float(df[df['symbol'] == token]['txCount'])
    not_stable_vol += float(df[df['symbol'] == token]['volumeUSD'])
    not_stable_fees += float(df[df['symbol'] == token]['feesUSD'])

df_grouped = pd.DataFrame([['Stablecoins', stable_tvl, stable_txcount, stable_vol, stable_fees],
                           ['Not Stablecoins', not_stable_tvl, not_stable_txcount, not_stable_vol, not_stable_fees]],
                         columns=['type', 'totalValueLockedUSD', 'txCount', 'volumeUSD', 'feesUSD'])

df_grouped.to_csv(f'uniswapTokens_grouped_{current_date}.csv', index=False)
