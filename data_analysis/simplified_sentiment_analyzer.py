import json
import statistics
import traceback

import pandas as pd
from transformers import pipeline
from typing import List, Dict, Any
from anyio import Path
from sentence_transformers import SentenceTransformer


from client.mongo_client import MONGO_CLIENT
from client.openai_client import get_topic_for_article
from config import CONFIG
from data_analysis.send_data_to_mongo import build_news_records


class SentimentAnalyzer:
    def __init__(self, model_name: str = "SamLowe/roberta-base-go_emotions"):
        try:
            self.classifier = pipeline(task="text-classification", model=model_name)
        except Exception as e:
            print(f"Failed to load model {model_name}: {e}")
            raise

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Perform sentiment analysis on the given text.

        Args:
            text (str): The text to analyze.

        Returns:
            Dict[str, float]: A dictionary containing the sentiment scores for each emotion.
        """
        return self.classifier(text)


async def analyze_news_sentiment():
    """

    :return:
    """
    usa_rows = await build_news_records("data/primer_hackathon_data_control.csv", "usa")
    # print(f"usa_rows {json.dumps(usa_rows, indent=4)}")
    china_rows = await build_news_records("data/primer_hackathon_data_china.csv", "china")
    # print(f"china_rows {json.dumps(china_rows, indent=4)}")
    russia_rows = await build_news_records("data/primer_hackathon_data_russia.csv", "russia")
    # print(f"russia_rows {json.dumps(russia_rows, indent=4)}")

    misinfocounter_database = MONGO_CLIENT["misinfocounter"]
    misinfocounter_collection = misinfocounter_database.get_collection("news_articles_sentiment_and_embeddings")

    usa_rows_filtered = usa_rows[:20]
    china_rows_filtered = usa_rows[:20]
    russia_rows_filtered = usa_rows[:20]
    # store in json
    await process_sentiment(usa_rows_filtered, SentimentAnalyzer())
    await process_sentiment(china_rows_filtered, SentimentAnalyzer())
    await process_sentiment(russia_rows_filtered, SentimentAnalyzer())

    usa_file_content = json.dumps(usa_rows_filtered, indent=4)
    await Path(CONFIG.root_path).joinpath("data/sentiment_usa.json").write_text(usa_file_content)
    china_file_content = json.dumps(china_rows_filtered, indent=4)
    await Path(CONFIG.root_path).joinpath("data/sentiment_china.json").write_text(china_file_content)
    russia_file_content = json.dumps(russia_rows_filtered, indent=4)
    await Path(CONFIG.root_path).joinpath("data/sentiment_russia.json").write_text(russia_file_content)

    # if misinfocounter_collection.count_documents({}) == 0:
    misinfocounter_collection.drop()
    misinfocounter_collection.insert_many(usa_rows)
    misinfocounter_collection.insert_many(china_rows)
    misinfocounter_collection.insert_many(russia_rows)
    # else:
    #     misinfocounter_collection.drop()
    #     print(f"not adding existing count: {misinfocounter_collection.count_documents({})}")
    #     print(f"records: {misinfocounter_collection.find()}")


def split_text_by_max_length(text, max_length):
    chunks = []
    while len(text) > max_length:
        # Find the nearest space to avoid cutting words
        split_index = text.rfind(' ', 0, max_length)
        if split_index == -1:  # No spaces found, forced to split at max_length
            split_index = max_length
        chunks.append(text[:split_index])
        text = text[split_index:].lstrip()  # Remove leading whitespace from the rest of the text
    chunks.append(text)  # Add what remains of the text as the last chunk
    return chunks


async def process_sentiment(rows: list[dict[str, Any]], analyzer: SentimentAnalyzer):
    counter = 0
    for row in rows:
        if not row["content"]:
            continue
        try:
            chunks = split_text_by_max_length(row["content"], 500)
            emotions = {}
            for chunk in chunks:
                sentiment = analyzer.analyze_sentiment(chunk)
                for emotion in sentiment:
                    label = emotion["label"]
                    if label not in emotions:
                        emotions[label] = []
                    emotions[label].append(emotion["score"])
            summarized_emotions = {}
            for label in emotions:
                summarized_emotions[label] = statistics.mean(emotions[label])
            row["sentiment"] = summarized_emotions
        except Exception as e:
            print(f"Failed to analyze sentiment: {e}")
            traceback.print_exc()
        model = SentenceTransformer('thenlper/gte-large')  # Load a pre-trained model
        row['embedding'] = [float(num) for num in model.encode(row["content"])]

        article_topic_feature = await get_topic_for_article({
            "title": row["title"],
            "content": row["content"],
        })
        print(f"article_topic_feature: {json.dumps(article_topic_feature, indent=4)}")
        if "major_topic" in article_topic_feature:
            row["llm_major_topic"] = article_topic_feature["major_topic"]
        if "entities" in article_topic_feature:
            row["llm_entities"] = article_topic_feature["entities"]
        if "people" in article_topic_feature:
            row["llm_people"] = article_topic_feature["people"]
        if "topics" in article_topic_feature:
            row["llm_topics"] = article_topic_feature["topics"]
        if "continent" in article_topic_feature:
            row["llm_continent"] = article_topic_feature["continent"]
        if "country" in article_topic_feature:
            row["llm_country"] = article_topic_feature["country"]

        counter += 1
