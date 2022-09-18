import requests
import posts_query
from retry import retry
from tqdm import tqdm

class LensFetcher:

    @retry(delay=1, backoff=2, max_delay=4, tries=5)
    def run_query(self, query):
        request = requests.post('https://api.lens.dev/graphql',
        json={'query': query}, headers={})
        if request.status_code == 200:
            return request.json()
        else:
            print ('exception raised')
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    def run_until_end(self, max_iterations = 50000000):
        total_count = 1 # dummy initialization for loop to start
        cursor = "{}"
        data_items = []
        iter_num = 0
        pbar = tqdm(total=max_iterations)
        while total_count > 0 and iter_num < max_iterations:
            #print ('total count {} cursor {} iter_num {}'.format(total_count, cursor, iter_num))
            # run query
            query_string = posts_query.get_query(cursor)
            # fetch total count
            result = self.run_query(query_string)
            items = result['data']['explorePublications']['items']
            data_items.extend(items)
            # update cursor
            cursor = result['data']['explorePublications']['pageInfo']['next']
            cursor = cursor.replace('"', '\\"')
            total_count = result['data']['explorePublications']['pageInfo']['totalCount']
            iter_num += 1
            pbar.update(1)
        pbar.close()
        return data_items
