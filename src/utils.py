import openai
import asyncio
from openai import OpenAI

with open('OPENAI_API_KEY', 'r') as file:
    client = OpenAI(api_key=file.readline().strip())

async def get_gpt4_response(config, assistant_prompt, text_prompt):
    completion = None
    message=[{"role": "assistant", "content": assistant_prompt}, {"role": "user", "content": text_prompt}]
    while completion is None:
        try:
            completion = client.chat.completions.create(
                model=config['model_name'],
                messages=message,
                max_tokens=config['max_tokens'],
                temperature=config['temperature']
            )
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__) 
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
          
    return completion.choices[0].message.content

