from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)