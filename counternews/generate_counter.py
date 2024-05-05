# Use LLM to generate a version of the article / article title that changes
# the tone/narrative from the original narrative
from openai import OpenAI
import os
import sys

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

def change_tone(article_text):
  response = client.chat.completions.create(
    model=MODEL,
    messages=[
      {
        "role": "system",
        "content": "You are a newspaper editor. You are submitted an article by a journalist that is either negative or positve on a topic. Your job is to rewrite it and change the sentiment from positie to negative or vice versa"
      },
      {
        "role": "user",
        "content": article_text
      }
    ],
    temperature=0.8,
    max_tokens=64,
    top_p=1
  )
  return response.choices[0].message.content


# test code

article_text="Donald Trump fell asleep once again during his hush money trial, including a 'critical' moment of proceedings, a legal expert has said.  Norm Eisen, who served as a special counsel to the House Judiciary Committee during the former president's first impeachment, told CNN that Trump was asleep in the New York court on Friday as his former White House aide Hope Hicks was answering questions under oath."
rewritten_text=change_tone (article_text)
print ('Original article: \n' + article_text)
print ('Rewritten article: \n' + rewritten_text)
