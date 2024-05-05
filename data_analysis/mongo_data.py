from client.mongo_client import MONGO_CLIENT


def get_news_source_groupings():
    misinfocounter_database = MONGO_CLIENT["misinfocounter"]
    misinfocounter_collection = misinfocounter_database.get_collection("news_article_sentiments")
    pipeline = [
        {
            "$group": {
                "source_name": "$source_name",  # Group by the 'source' field
                "count": {"$sum": 1}  # Count the occurrences of each source
            }
        },
        {
            "$sort": {"count": -1}  # Optional: sort by the count, descending
        }
    ]

    results = misinfocounter_collection.aggregate(pipeline)
    return results

