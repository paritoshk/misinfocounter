import csv
import io
import json
import pickle

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
        misinfocounter_collection.delete_many()
        misinfocounter_collection.insert_many(usa_rows)
        misinfocounter_collection.insert_many(china_rows)
        misinfocounter_collection.insert_many(russia_rows)
    else:
        # misinfocounter_collection.delete_many()
        print(f"not adding existing count: {misinfocounter_collection.count_documents({})}")
        print(f"records: {misinfocounter_collection.find()}")


async def send_news_article_data_to_mongo_with_sentiments():
    """

    """
    usa_rows = build_pickle_news_records("data/df_control.pkl", "usa")
    # print(f"usa_rows {json.dumps(usa_rows, indent=4)}")
    # china_rows = await build_pickle_news_records("data/df_china.pkl", "china")
    # print(f"china_rows {json.dumps(china_rows, indent=4)}")
    # russia_rows = await build_pickle_news_records("data/df_russia.pkl", "russia")
    # print(f"russia_rows {json.dumps(russia_rows, indent=4)}")

    misinfocounter_database = MONGO_CLIENT["misinfocounter"]
    misinfocounter_collection = misinfocounter_database.get_collection("news_article_sentiments")

    if misinfocounter_collection.count_documents({}) == 0:
        # misinfocounter_collection.delete_many()
        misinfocounter_collection.insert_many(usa_rows)
        # misinfocounter_collection.insert_many(china_rows)
        # misinfocounter_collection.insert_many(russia_rows)
    else:
        print(f"not adding existing count: {misinfocounter_collection.count_documents({})}")
        print(f"records: {misinfocounter_collection.find()}")


def build_pickle_news_records(path: str, country: str):
    pickle_path = str(Path(CONFIG.root_path, "data/df_control.pkl"))
    vectorizer = pickle.load(open(pickle_path, "rb"))

    all_rows_as_dicts = [row.to_dict() for index, row in vectorizer.iterrows()]
    for row in all_rows_as_dicts:
        row["country"] = country

        # TODO: generate embedding of title and content
        row["embedding"] =

    return all_rows_as_dicts


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
