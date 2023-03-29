
import openai


openai.api_key = ""

try:
#    print(openai.Model.list())
    print('ok')
except Exception as e:
    print(f"Error: {e}")

MODEL='gpt-3.5-turbo-0301'
#MODEL='text-davinci-003'
# example with a system message
response = openai.ChatCompletion.create(
#response = openai.Completion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "can you tell me something about MLOps."},
    ],
    temperature=0,
    max_tokens=100,
)

print(response['choices'][0]['message']['content'])
