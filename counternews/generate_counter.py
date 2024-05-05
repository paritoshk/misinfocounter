# Use LLM to generate a version of the article / article title that changes
# the tone/narrative from the original narrative
import json

import torch
from anyio import Path

from openai import OpenAI
import os
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from client.mongo_client import MONGO_CLIENT
from config import CONFIG

OPENAPI_URL=os.environ.get('OPENAPI_URL')
OPENAPI_KEY=os.environ.get('OPENAPI_KEY')
MODEL=os.environ.get('MODEL')

if OPENAPI_URL is None or OPENAPI_URL == '':
  print('Error: OPENAPI_URL environment variable is not set.')
  sys.exit(1)

if OPENAPI_KEY is None or OPENAPI_KEY == '':
  print('Error: OPENAPI_KEY environment variable is not set.')
  sys.exit(1)

if MODEL is None or MODEL == '':
  print('Error: MODEL environment variable is not set.')
  sys.exit(1)


client = OpenAI(
    base_url=OPENAPI_URL,
    api_key=OPENAPI_KEY,
)

#PROMPT=f"You are a newspaper editor. You are submitted an article by a journalist in your team. Your job is to rewrite it and change the sentiment more {TONE}"

async def find_articles(topic: str):
  # Example embeddings normalized for cosine similarity
  model = SentenceTransformer('thenlper/gte-small')  # Load a pre-trained model
  topic_embedding = [float(num) for num in model.encode(topic)]

  misinfocounter_database = MONGO_CLIENT["misinfocounter"]
  misinfocounter_collection = misinfocounter_database.get_collection(
    "news_articles_sentiment_and_embeddings")

  china_articles_found = await find_articles_for_country_with_torch("china", topic_embedding)
  russia_articles_found = await find_articles_for_country_with_torch("russia", topic_embedding)

  return china_articles_found + russia_articles_found

async def find_articles_for_country_with_faiss(country, topic_embedding):
  """

  :param country:
  :param topic_embedding:
  :return:
  """
  json_file_for_import = Path(CONFIG.root_path).joinpath(f"data/sentiment_{country}.json")
  articles_text = await json_file_for_import.read_text()
  articles = json.loads(articles_text)

  index = faiss.IndexHNSWFlat(384, 3)  # 10 is the number of neighbors in the HNSW graph
  for article in articles:
    query = np.array(article["embedding"], dtype='float32').reshape(1, -1)
    index.add(query)

  topic_query = np.array(topic_embedding, dtype='float32').reshape(1, -1)

  print(f"finding_articles via hnswindex")
  D, indices = index.search(topic_query, k=3)  # find the 2 nearest neighbors
  print("done finding articles")

  filtered_articles = []
  for index in indices:
    filtered_articles.append(articles[index])

  return filtered_articles

async def find_articles_for_country_with_torch(country, topic_embedding):
  """

  :param country:
  :param topic_embedding:
  :return:
  """
  json_file_for_import = Path(CONFIG.root_path).joinpath(f"data/sentiment_{country}.json")
  articles_text = await json_file_for_import.read_text()
  articles = json.loads(articles_text)

  article_embeddings = []
  for article in articles:
    article_embeddings.append(article["embedding"])

  data = torch.tensor(article_embeddings, dtype=torch.float32)
  query = torch.tensor([topic_embedding], dtype=torch.float32)  # Make the query two-dimensional

  data_norm = data / data.norm(dim=1, keepdim=True)
  query_norm = query / query.norm(dim=1, keepdim=True)
  # Compute cosine similarities using matrix multiplication
  cos_similarities = torch.mm(query_norm, data_norm.transpose(0, 1))
  # Extract top 3 nearest neighbors based on cosine similarities
  top_n_values, indices = torch.topk(cos_similarities, 3, largest=True)

  filtered_articles = []
  for index in indices.tolist()[0]:
    filtered_articles.append(articles[index])

  return filtered_articles


async def change_tone(tone, word_count, topic):
  print(f"refuting: `{topic}` with {tone} tone up to {word_count} words")
  system_prompt = f"You are government official, responding to the news article published with a response that is {tone} in tone. Keep your response down to {word_count} word count."

  china_articles = await find_articles(topic)

  china_articles_filtered = []
  for article in china_articles:
    china_articles_filtered.append({
      "title": article["title"],
      "content": article["content"],
      "country": article["country"],
    })
  article_string = json.dumps(china_articles_filtered)
  user_prompt_text = (f"The topic at hand is {topic} and the following articles have been written by our adversaries:\n"
                      f"{article_string}")

  print(f"sending prompt to openai")
  response = client.chat.completions.create(
    model=MODEL,
    messages=[
      {
        "role": "system",
        "content": system_prompt
      },
      {
        "role": "user",
        "content": user_prompt_text
      }
    ],
    temperature=0.8,
    max_tokens=500,
    top_p=1
  )

  response = response.choices[0].message.content

  references = "References:\n"
  for article in china_articles:
    references += f"""
      - {article["country"]}: {article["source_name"]} {article["title"]}
        URL: {article["original_url"]} 
        Major Topic: {article["llm_major_topic"]}
        Topics: {",".join(article["llm_topics"])}
        Sentiment: {",".join(article["sentiment"])}
        Entities Discussed: {",".join(article["llm_entities"])}
        People Discussed: {",".join(article["llm_people"])}
        "
    """
  return response + "\n\n\n" + references


# test code

# article_text=" Jan. 10 (Xinhua) -- The maritime authority of the Australian state of New South Wales (NSW) has warned personal watercraft users to keep cautious on water after a statewide safety blitz was conducted over the weekend.  In a statement released on Monday, NSW Maritime said that during the two-day Operation Ride Smart campaign, officers checked nearly 2,200 recreational vessels, including jetskis, which resulted in a total of 78 fines and 236 official warnings.  'Since the start of the boating season on Oct. 1, 2022, across NSW we've recorded more than 120 incidents including a boat fire, boats capsizing, collisions and multiple water rescues where serious injuries were reported. Tragically, there have also been four boating-related fatalities,' said NSW Maritime Acting Executive Director Hendrik Clasie.  'Jetskis are heavily overrepresented in serious boating incidents and complaints,' Clasie said, noting that the top three offenses over the weekend were unlicensed operation of a jetski, irregular riding, and not cooperating with compliance checks.  'We love to see locals and holidaymakers enjoying our state's waterways, but people need to be aware they are in a different condition following months of severe rainfall and flooding. We're seeing more debris and unseen hazards, including entire trees,' said the director.  He called on watercraft users to remember care, courtesy and common sense, especially when there are swimmers, surfers or paddle boarders around.  According to the NSW Maritime, there are currently more than 82,000 licensed riders in the state, with nearly 20,000 personal watercrafts registered. ' "
#
# rewritten_text=change_tone("angry", 500)
# print ('Original article: \n' + article_text)
# print ('Rewritten article: \n' + rewritten_text)
