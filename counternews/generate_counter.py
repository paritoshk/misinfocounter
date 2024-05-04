from openai import OpenAI

client = OpenAI(
    base_url="",
    api_key="",
)

prompt_text = "Once upon a time, in a far-off land, there was a brave knight"

# Call OpenAI API to generate text
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

# Print the generated text
print(response)

