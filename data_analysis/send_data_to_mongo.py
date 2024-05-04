from client.mongo_client import MONGO_CLIENT


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

