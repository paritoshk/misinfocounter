import csv
import io
import json

import pandas
from typing import Any

from client.mongo_client import MONGO_CLIENT

from anyio import Path

from config import CONFIG


def send_test_data_to_mongo():
    """

    :return:
    """
    test_database = MONGO_CLIENT["test"]
    test_collection = test_database.get_collection("test_collection")
    test_data = test_collection.find_one({"key": "test1"})

    if not test_data:
        test_collection.insert_one({
            "key": "test1",
            "topic": "test"
        })
        test_data = test_collection.get_one({"key": "test1"})

    print(f"test_data {test_data}")


async def send_news_article_data_to_mongo_raw():
    """

    """
    usa_rows = await build_news_records("data/primer_hackathon_data_control.csv", "usa")
    # print(f"usa_rows {json.dumps(usa_rows, indent=4)}")
    china_rows = await build_news_records("data/primer_hackathon_data_china.csv", "china")
    # print(f"china_rows {json.dumps(china_rows, indent=4)}")
    russia_rows = await build_news_records("data/primer_hackathon_data_russia.csv", "russia")
    # print(f"russia_rows {json.dumps(russia_rows, indent=4)}")

    misinfocounter_database = MONGO_CLIENT["misinfocounter"]
    misinfocounter_collection = misinfocounter_database.get_collection("news_articles_raw")

    if misinfocounter_collection.count_documents({}) == 0:
        misinfocounter_collection.insert_many(usa_rows)
        misinfocounter_collection.insert_many(china_rows)
        misinfocounter_collection.insert_many(russia_rows)
    else:
        print(f"not adding existing count: {misinfocounter_collection.count_documents({})}")


async def build_news_records(path: str, country: str) -> list[dict[str, Any]]:
    # Prints the first five rows of the DataFrame, including headers
    # news_data = await Path(CONFIG.root_path).joinpath(path).read_text()
    news_rows: list[Any] = []
    # Read data using csv.DictReader
    news_path = Path(CONFIG.root_path).joinpath(path)
    dataframe = pandas.read_csv(str(news_path))
    for index, row in dataframe.iterrows():
        model_row = row.dropna().to_dict()

        # Source Name,Date,Original URL,Title,Content
        news_row = {
            "country": country,
            "source_name": None,
            "date": None,
            "original_url": None,
            "title": None,
            "content": None,
            "sentiment": None,
            "topics": None,
        }
        if "Source Name" in model_row:
            news_row["source_name"] = model_row["Source Name"]
        if "Date" in model_row:
            news_row["date"] = model_row["Date"]
        if "Original URL" in model_row:
            news_row["original_url"] = model_row["Original URL"]
        if "Title" in model_row:
            news_row["title"] = model_row["Title"]
        news_rows.append(news_row)

    return news_rows
