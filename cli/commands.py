import asyncio

import click

from data_analysis.send_data_to_mongo import send_test_data_to_mongo, \
    send_news_article_data_to_mongo_raw, send_news_article_data_to_mongo_with_sentiments, \
    use_llm_to_add_topic_features, create_embeddings_for_documents, \
    create_embeddings_for_raw_documents, import_new_article_file_to_mongo
from data_analysis.simplified_sentiment_analyzer import analyze_news_sentiment
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

    @cli.command("add_embeddings_to_articles")
    def add_embeddings_to_articles():
        asyncio.run(create_embeddings_for_documents())

    @cli.command("add_embeddings_to_articles_for_raw")
    def add_embeddings_to_articles_for_raw():
        asyncio.run(create_embeddings_for_raw_documents())

    @cli.command("analyze_sentiment")
    def analyze_sentiment():
        asyncio.run(analyze_news_sentiment())

    @cli.command("refute_article_via_llm")
    @click.argument("tone")
    @click.argument("word_count")
    @click.argument("topic")
    def refute_article_via_llm(tone: str, word_count: int, topic: str):
        from counternews.generate_counter import change_tone
        response = asyncio.run(change_tone(tone, word_count, topic))
        print(f"RESPONSE for tone {tone}\n\n{response}")

    @cli.command("import_new_file_to_mongo_articles")
    @click.argument("file")
    def import_new_file_to_mongo_articles(file: str):
       asyncio.run(import_new_article_file_to_mongo(file))
