import json

from bertopic import BERTopic

# Optional for additional processing
import pandas as pd

from anyio import Path

from config import CONFIG


async def run_news_topic_model():
    print("running news_topic_model")
    # Example: Loading from a CSV file
    print(f"ROOT_DIR: {CONFIG.root_path}")
    news_data_path = str(Path(CONFIG.root_path).joinpath("data/primer_hackathon_data_control.csv"))
    df = pd.read_csv(news_data_path)
    print("data loaded")

    texts = df['Title'].tolist()

    print("Title list created")
    topic_model = BERTopic(language="english", calculate_probabilities=True)
    topics, probabilities = topic_model.fit_transform(texts)
    print("topics created")

    # Get an overview of the topics found
    topic_info = topic_model.get_topic_info()
    print(f"topic count: {len(topics)}")
    print(f"topics: {topics}")
    print(f"topic_info: {topic_info}")

    topics = topic_model.get_topics()
    topic_file_content = json.dumps(topics, indent=4)
    await Path(CONFIG.root_path).joinpath("data/control_topics.json").write_text(topic_file_content)

    # Create a DataFrame
    df = pd.DataFrame({
        'Text': texts,
        'Topic': topics,
        'Probability': probabilities  # Omit if probabilities were not calculated
    })

    # Now you can manipulate or analyze the DataFrame based on topics
    print(df.head())

    # Retrieve individual topics
    # topic_1 = topic_model.get_topic(1)  # Replace '5' with the topic number you are interested in
    # topic_5 = topic_model.get_topic(5)  # Replace '5' with the topic number you are interested in
    # print(f"topic 1: {topic_1}")
    # print(f"topic 5: {topic_5}")

    # Visualizing topics with their probabilities
    # topic_model.visualize_topics()

    # Visualizing topic probabilities over the entire corpus
    # topic_model.visualize_distribution(probabilities[0], min_probability=0.010)

    # Visualize the terms for a single topic
    # topic_model.visualize_barchart(topic=5)

    # Saving the model
    # topic_model.save("path_to_save_model")

    # Loading the model
    # loaded_model = BERTopic.load("path_to_save_model")

    # if we want to adjust the topic
    # adjusted_topic_model = BERTopic(nr_topics='auto')
    # topics, probabilities = adjusted_topic_model.fit_transform(texts)
