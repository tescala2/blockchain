import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from requests import post
from datetime import date


current_date = date.today()

def helper(payload, rpc):
    r = post(rpc, json=payload)
    j = r.json()

    return j

rpc_v3 = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

ids = ["0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640", "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"]

df_list = []

for i in ids:
    graphql_query = """
    {
      pool(id: "%s") {
        id
        feeTier
        poolDayData(first: 1000) {
          date
          volumeUSD
          feesUSD
          tvlUSD
          txCount
        }
      }
    }
    """ % i

    payload = {
        "query": graphql_query,
        }

    j = helper(payload, rpc_v3)

    df = pd.json_normalize(j['data']['pool']['poolDayData'])
    df['feeTier'] = float(j['data']['pool']['feeTier'])
    df_list.append(df)

df = pd.concat(df_list)
df['date'] = pd.to_datetime(df['date'], unit='s')

df.to_csv(f'uniswapPools_ETH_USDC_{current_date}.csv')

x_3000 = df.loc[df['feeTier'] == 3000, 'date'].to_numpy()
y_3000 = df.loc[df['feeTier'] == 3000, 'volumeUSD'].to_numpy()
y_3000 = np.array([float(y) for y in y_3000])

x_500 = df.loc[df['feeTier'] == 500, 'date'].to_numpy()
y_500 = df.loc[df['feeTier'] == 500, 'volumeUSD'].to_numpy()
y_500 = np.array([float(y) for y in y_500])

plt.figure()
plt.plot(x_3000, y_3000, label='0.3% fee')
plt.plot(x_500, y_500, label='0.05% fee')
plt.xlabel('Date')
plt.ylabel('Volume (USD)')
plt.legend()
plt.title("Comparing UniswapV3's ETH/USDC Pools")

plt.savefig('uniswapPools_ETH_USDC')
plt.show()
