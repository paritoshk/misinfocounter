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

#PROMPT=f"You are a newspaper editor. You are submitted an article by a journalist in your team. Your job is to rewrite it and change the sentiment more {TONE}"

def change_tone(tone, word_count):
  system_prompt = f"You are government official, responding to the news article published with a response that is {tone} in tone. Keep your response down to {word_count} word count."
  user_prompt_text = """
  Jan. 10 (Xinhua) -- The maritime authority of the Australian state of New South Wales (NSW) has warned personal watercraft users to keep cautious on water after a statewide safety blitz was conducted over the weekend.

In a statement released on Monday, NSW Maritime said that during the two-day Operation Ride Smart campaign, officers checked nearly 2,200 recreational vessels, including jetskis, which resulted in a total of 78 fines and 236 official warnings.

""Since the start of the boating season on Oct. 1, 2022, across NSW we've recorded more than 120 incidents including a boat fire, boats capsizing, collisions and multiple water rescues where serious injuries were reported. Tragically, there have also been four boating-related fatalities,"" said NSW Maritime Acting Executive Director Hendrik Clasie.

""Jetskis are heavily overrepresented in serious boating incidents and complaints,"" Clasie said, noting that the top three offenses over the weekend were unlicensed operation of a jetski, irregular riding, and not cooperating with compliance checks.

""We love to see locals and holidaymakers enjoying our state's waterways, but people need to be aware they are in a different condition following months of severe rainfall and flooding. We're seeing more debris and unseen hazards, including entire trees,"" said the director.

He called on watercraft users to remember care, courtesy and common sense, especially when there are swimmers, surfers or paddle boarders around.

According to the NSW Maritime, there are currently more than 82,000 licensed riders in the state, with nearly 20,000 personal watercrafts registered. ■"
"""
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
  return response.choices[0].message.content


# test code

# article_text=" Jan. 10 (Xinhua) -- The maritime authority of the Australian state of New South Wales (NSW) has warned personal watercraft users to keep cautious on water after a statewide safety blitz was conducted over the weekend.  In a statement released on Monday, NSW Maritime said that during the two-day Operation Ride Smart campaign, officers checked nearly 2,200 recreational vessels, including jetskis, which resulted in a total of 78 fines and 236 official warnings.  'Since the start of the boating season on Oct. 1, 2022, across NSW we've recorded more than 120 incidents including a boat fire, boats capsizing, collisions and multiple water rescues where serious injuries were reported. Tragically, there have also been four boating-related fatalities,' said NSW Maritime Acting Executive Director Hendrik Clasie.  'Jetskis are heavily overrepresented in serious boating incidents and complaints,' Clasie said, noting that the top three offenses over the weekend were unlicensed operation of a jetski, irregular riding, and not cooperating with compliance checks.  'We love to see locals and holidaymakers enjoying our state's waterways, but people need to be aware they are in a different condition following months of severe rainfall and flooding. We're seeing more debris and unseen hazards, including entire trees,' said the director.  He called on watercraft users to remember care, courtesy and common sense, especially when there are swimmers, surfers or paddle boarders around.  According to the NSW Maritime, there are currently more than 82,000 licensed riders in the state, with nearly 20,000 personal watercrafts registered. ' "
#
# rewritten_text=change_tone("angry", 500)
# print ('Original article: \n' + article_text)
# print ('Rewritten article: \n' + rewritten_text)
