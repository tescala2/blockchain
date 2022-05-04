import pandas as pd
from requests import post
from datetime import date

current_date = date.today()

def helper(payload, rpc):
    r = post(rpc, json=payload)
    j = r.json()

    return j

rpc_v3 = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

graphql_query = """
{
  uniswapDayDatas(orderBy: date, first: 500) {
    date
    feesUSD
    tvlUSD
    volumeUSD
    txCount
  }
}
"""

payload = {
    "query": graphql_query,
    }

j = helper(payload, rpc_v3)

df = pd.json_normalize(j['data']['uniswapDayDatas'])
df['date'] = pd.to_datetime(df['date'], unit='s')

df.to_csv(f'uniswapDayData_{current_date}.csv', index=False)