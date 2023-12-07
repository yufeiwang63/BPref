from openai import OpenAI
import base64
import os
from copilot_infer import extract_anwser

list_of_api_keys = [
   os.environ['YUFEI_OPENAI_API_KEY'],
   os.environ['YUFEI2_OPENAI_API_KEY'],
#    os.environ['YUFEI3_OPENAI_API_KEY'],
]

global api_key_idx, cnt
api_key_idx = 0
cnt = 0

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def api_call(img_path, prompt):
    client = OpenAI()
    base64_image = encode_image(img_path)
    response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    }
                ],
                }
            ],
            max_tokens=300,
            temperature=0.0,
        )
    return response

def gpt4v_infer(prompt, img_path):
    global api_key_idx
    try:
        os.environ['OPENAI_API_KEY'] = list_of_api_keys[api_key_idx]
        response = api_call(img_path, prompt)
    except:
        api_key_idx = (api_key_idx + 1) 
        if api_key_idx >= len(list_of_api_keys):
           return -1
        os.environ['OPENAI_API_KEY'] = list_of_api_keys[api_key_idx]
        response = api_call(img_path, prompt)
        
    result = ''
    for choice in response.choices:
        result += choice.message.content

    print(result)
    result = result.split("\n")
    result = [line.lower() for line in result]
    return extract_anwser(result)

if __name__ == "__main__":
    prompt = """
There are two images I will show to you. They are both about the task of "balancing the cartpole", where a pole is attached to a cart, and the goal is to balance the pole upright on the cart without falling down. The task is considered to be better achieved if the tilt angle of the pole is small from being upright vertical.
Please response which of the two images you think better achieves the goal.
Please Think step by step.
Please first reply with your reasoning, and then followed by a single line with "output: first" or "output: second".

Example:
Input: [two images where the pole in the first image is tilting a lot towards right], There are two images ...
Output:
I think the cartpole in the second image achieves the task better because it has a smaller tilt angle. [More reasoning here]
output: second

Another example:
Input: [two image where the pole in the second image is tilting towards left], There are two cartpoles ...
Output:
I think the cartpole in the first image achieves the task better because it is more upright compared to the second one, which is tileting towards left. [More reasoning here]
output: first
"""
    gpt4v_infer(prompt, img_path)