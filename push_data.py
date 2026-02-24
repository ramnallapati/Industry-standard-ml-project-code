import os
import sys
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()


class NetworkDataExtract():

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = data.to_dict(orient='records')
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            if MONGO_DB_URL is None:
                raise ValueError("Mongo DB URL not found")

            mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            db = mongo_client[database]
            collection_obj = db[collection]

            collection_obj.insert_many(records)

            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


# Execution part
if __name__ == "__main__":

    FILE_PATH = "Network_Data/WebsitePhishing.csv"
    DATABASE = "RAM_NALLAPATI"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()

    records = networkobj.csv_to_json_converter(FILE_PATH)

    no_of_records = networkobj.insert_data_mongodb(
        records,
        DATABASE,
        COLLECTION
    )

    print(f'No of records inserted: {no_of_records}')