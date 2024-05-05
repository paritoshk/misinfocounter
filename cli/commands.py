import asyncio

import click

from data_analysis.send_data_to_mongo import send_test_data_to_mongo, \
    send_news_article_data_to_mongo_raw
from topic_models.news_source_topic_model import run_news_topic_model


def add_cli_commands(cli):
    """

    :param cli:
    :return:
    """

    @cli.command("run_topic_model")
    def run_topic_model():
        """
        run the topic model

        :return:
        """
        asyncio.run(run_news_topic_model())

    @cli.command("analyze_sentiment")
    async def analyze_sentiment():
        """

        :return:
        """

    @cli.command("test_send_data_to_mongo")
    def test_send_data_to_mongo():
        test_collection = send_test_data_to_mongo()

    @cli.command("send_news_article_data_to_mongo")
    def send_news_article_data_to_mongo():
        asyncio.run(send_news_article_data_to_mongo_raw())
