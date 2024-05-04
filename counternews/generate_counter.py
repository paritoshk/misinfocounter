# Use LLM to generate a version of the article / article title that changes
# the tone/narrative from the original narrative

from openai import OpenAI

client = OpenAI(
    base_url="",
    api_key="",
)

def change_tone (article_text):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
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
