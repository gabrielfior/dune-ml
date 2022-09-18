from S3Storer import S3Storer
from lens_fetcher import LensFetcher

if __name__ == "__main__":
    # fetch lens data
    lf = LensFetcher()
    results = lf.run_until_end(2000) #:9650 max iterations

    # store in s3
    s3storer = S3Storer('PUBLICATIONS_v3')
    s3storer.store_json_inside_bucket(results)