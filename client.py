from openai import OpenAI
import os
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")),

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named Nova skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)