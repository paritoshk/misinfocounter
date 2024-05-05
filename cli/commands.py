import asyncio

from data_analysis.send_data_to_mongo import send_test_data_to_mongo, \
    send_news_article_data_to_mongo_raw, send_news_article_data_to_mongo_with_sentiments, \
    use_llm_to_add_topic_features
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

    @cli.command("send_news_article_data_to_mongo_as_raw")
    def send_news_article_data_to_mongo_as_raw():
        asyncio.run(send_news_article_data_to_mongo_raw())

    @cli.command("send_news_article_data_to_mongo_sentimented")
    def send_news_article_data_to_mongo_sentimented():
        asyncio.run(send_news_article_data_to_mongo_with_sentiments())

    @cli.command("add_topics_to_articles_via_llm")
    def add_topics_to_articles_via_llm():
        asyncio.run(use_llm_to_add_topic_features())
