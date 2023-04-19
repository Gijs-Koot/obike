import os
import datetime
import boto3
import json
import requests


BUCKETNAME = os.environ["BUCKETNAME"]
URL = "http://fiets.openov.nl/locaties.json"
LOCALFN = "/tmp/obike-latest.json"

s3_client = boto3.client("s3")


def get_key():
    return datetime.datetime.now().strftime("%Y-%m-%d/%H:%M:%S.json")


def lambda_handler(event, context):

    dt = requests.get(URL).json()
    with open(LOCALFN, "w") as f:
        json.dump(dt, f)

    key = get_key()
    s3_client.upload_file(LOCALFN, BUCKETNAME, key)

    print(f"Saved data to {key}")


if __name__ == "__main__":

    lambda_handler(None, None)
