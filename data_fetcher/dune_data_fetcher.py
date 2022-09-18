import os
from dotenv import load_dotenv
import pathlib
parent_path = pathlib.Path(__file__).parent.resolve().parent
load_dotenv(parent_path.joinpath('.env'))
from dune_client.client import DuneClient
from dune_client.query import Query

class DuneDataFetcher:

    BASE_URL = "https://api.dune.com/api/v1/"

    def __init__(self):
        self.dune = DuneClient(os.environ["DUNE_API_KEY"])
        
    def get_results_from_query(self, query_id):
        query = Query(
        name="my_query", query_id=query_id)
        print("Results available at", query.url())
        self.dune.execute(query)
        results = self.dune.refresh(query)
        return results