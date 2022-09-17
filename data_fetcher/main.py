from S3Storer import S3Storer
from lens_fetcher import LensFetcher

if __name__ == "__main__":
    # fetch lens data
    lf = LensFetcher()
    results = lf.run_until_end(max_iterations=500) #:9250 max offset

    # store in s3
    s3storer = S3Storer()
    s3storer.store_json_inside_bucket(results)