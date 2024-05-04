from openai import OpenAI

client = OpenAI(
    base_url="https://hackathon.radiantai.com/misinfocounter/openai",
    api_key="rad-e3c09efb1e702d4f6810e51df2c9724185b106dfe24154ec54c048d2e9f11940-iant",
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

