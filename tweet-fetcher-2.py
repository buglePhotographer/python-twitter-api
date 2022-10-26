import requests
import configparser
import configparser
import pandas as pd
import time

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'BEARER TOKEN'

search_url = "https://api.twitter.com/2/tweets/search/all"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
# query_params = {
#     'query': '(from:horaciorlarreta) to:2019-12-10 from:2019-12-01'}

query_params = {
    'query': '(from:horaciorlarreta)',
    'start_time': '2015-01-01T00:00:00-03:00',
    'end_time': '2019-12-10T23:59:00-03:00',
    'tweet.fields': 'created_at'
}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request(
        "GET", search_url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():

    columns = ['Usuario', 'Fecha de publicación', 'Tweet']
    data = []

    next_token = ''

    name = 'horaciorlarreta'

    try:

        while True:

            if next_token:
                query_params['next_token'] = next_token
                next_token = ''

            page = connect_to_endpoint(search_url, query_params)

            if 'meta' in page and 'next_token' in page['meta']:
                next_token = page['meta']['next_token']

            for tweet in page['data']:

                if tweet['created_at']:
                    created_at = tweet['created_at'].split('T')[0]

                if tweet['text']:
                    tweet_text = tweet['text']

                data.append([name, created_at, tweet_text])

            print('Pagina terminada')
            time.sleep(5)

            if not next_token:
                break

    except Exception as e:
        print(e)
        pass

    df = pd.DataFrame(data, columns=columns)

    df.to_excel('tweets_larreta.xlsx', sheet_name='horaciorlarreta')

    print('Terminado')


if __name__ == "__main__":
    main()
