import json


def load_search_data():

    with open(
        "testdata/search_data.json",
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data["search_terms"]