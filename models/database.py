from enum import Enum


class DATBASE_ACTIONS(str, Enum):
    insert = "insert"
    fetch_one = "fetch_one"
    fetch_all = "fetch_all"
    delete = "delete"
