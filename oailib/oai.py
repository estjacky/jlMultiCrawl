
import openai


openai.api_key = "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"

try:
#    print(openai.Model.list())
    print('ok')
except Exception as e:
    print(f"Error: {e}")

MODEL='text-davinci-003'
# example with a system message
response = openai.Completion.create(
    model=MODEL,
#    prompt="Explain MLops",
    prompt="Explain LUIS in NLP",
    temperature=0,
    max_tokens=100,
    n=1,
    stream=False
)

print(response['choices'][0]['text'])
