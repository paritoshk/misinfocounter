import json
from collections import Counter

from anyio import Path

from client.openai_client import client
from config import CONFIG


async def get_country_articles(country):
    json_file_for_import = Path(CONFIG.root_path).joinpath(f"data/sentiment_{country}.json.bak")
    articles_text = await json_file_for_import.read_text()
    return json.loads(articles_text)


async def find_most_common_topics():
    """

    :return:
    """
    china_articles = await get_country_articles("china")
    topic_list = []
    for article in china_articles:
        if "llm_topics"in article:
            topic_list.extend(article["llm_topics"])
    russia_articles = await get_country_articles("russia")
    topic_list = []
    for article in russia_articles:
        if "llm_topics"in article:
            topic_list.extend(article["llm_topics"])

    print(topic_list)

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are being provided a list of topics, reply back with the most commonly mentioned topics normalized. Make sure that they are ordered in terms of the most common and provide the number of times it is provided.",
            },
            {
                "role": "user",
                "content": json.dumps(topic_list),
            }
        ],
        model="gpt-3.5-turbo-0125",
    )
    chat_completion = str(chat_completion.choices[0].message.content)
    print(f"most common topics: {chat_completion}")

    # Count the frequency of each topic using Counter
    topic_counts = Counter(topic_list)

    # Sort topics by frequency in descending order
    sorted_topics = topic_counts.most_common()  # most_common() sorts items by the frequency in descending order

    return sorted_topics
