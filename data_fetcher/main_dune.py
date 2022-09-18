from dune_data_fetcher import DuneDataFetcher
from S3Storer import S3Storer

if __name__ == "__main__":
    # fetch dune queries
    # store as S3 obj
    ddf = DuneDataFetcher()
    #s3storer = S3Storer('DUNE_wallets_per_day')
    #query_wallets_per_day = '781918'
    #results_wallets = ddf.get_results_from_query(query_wallets_per_day)
    #s3storer.store_json_inside_bucket(results_wallets)

    s3storer = S3Storer('DUNE_followers_followee')
    
    query_followers = '1279759'
    results_followers = ddf.get_results_from_query(query_followers)
    s3storer.store_json_inside_bucket(results_followers)