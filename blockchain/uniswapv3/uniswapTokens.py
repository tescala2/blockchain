import pandas as pd
from requests import post
from datetime import date

current_date = date.today()

def helper(payload, rpc):
    r = post(rpc, json=payload)
    j = r.json()

    return j

rpc_v3 = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

df_list = []
for i in [1000, 2000, 3000, 4000]:
    graphql_query_ids = """
    {
      tokens(first: 1000, skip: %s) {
        name
        id
      }
    }
    """ % i

    payload_ids = {
        "query": graphql_query_ids
    }

    j = helper(payload_ids, rpc_v3)

    for token in j['data']['tokens']:
        token_id = token['id']
        graphql_query_token = """
        {
          token(id: "%s") {
            name
            symbol
            totalValueLockedUSD
            txCount
            volumeUSD
            feesUSD
          }
        }
        """ % token_id

        payload_token = {
            "query": graphql_query_token
        }

        j = helper(payload_token, rpc_v3)

        df = pd.json_normalize(j['data']['token'])
        df_list.append(df)

df = pd.concat(df_list)
df = df.sort_values(by='volumeUSD', ascending=False)
df = df.head(8)

df.to_csv(f'uniswapTokens_{current_date}.csv', index=False)
