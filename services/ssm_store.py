import os

import boto3

OFFLINE = os.environ.get("OFFLINE") == "true"
ENVIRONMENT = os.environ["ENVIRONMENT"]


def get_parameter(
    parameter: str,
) -> str:
    if OFFLINE:
        return os.environ[parameter]

    client = boto3.client("ssm")
    value = client.get_parameter(
        Name=f"/RECIPE_AI_{ENVIRONMENT}/{parameter}",
        WithDecryption=True,
    )[
        "Parameter"
    ]["Value"]
    return value
