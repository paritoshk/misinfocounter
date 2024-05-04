import asyncio

import click

from data_analysis.send_data_to_mongo import send_test_data_to_mongo
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


    @cli.command("send_data_to_mongo")
    def send_data_to_mongo():
        test_collection = send_test_data_to_mongo()
