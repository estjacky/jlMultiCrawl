
import openai


openai.api_key ="YOURKEYHERE" 

try:
#    print(openai.Model.list())
    print('ok')
except Exception as e:
    print(f"Error: {e}")

mytext="NASA awarded Elon Musk’s SpaceX a $2.9 billion contract to build the lunar lander."

MODEL='text-davinci-003'
# example with a system message
response = openai.Completion.create(
    model=MODEL,
#    prompt="Explain MLops",
    prompt=f"Extracts entities and entities type from '{mytext}'",
    temperature=0,
    max_tokens=100,
    n=1,
    stream=False
)

print(response['choices'][0]['text'])
