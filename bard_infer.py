from bardapi import Bard
import os
import requests
from copilot_infer import extract_anwser
import time

os.environ['_BARD_API_KEY'] = 'dwj7ZkMiCf9JQAEDXaYQSJtSNMgZMMKbF9J7kAarpWfcI7ojXB8deBtpvbRH_KPhCmw8ag.'

def bard_query_session(prompts, images):
    session = requests.Session()
    session.headers = {
                "Host": "bard.google.com",
                "X-Same-Domain": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Origin": "https://bard.google.com",
                "Referer": "https://bard.google.com/",
            }
    session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 

    bard = Bard(token=os.environ['_BARD_API_KEY'], session=session, timeout=60)

    responses = []
    for idx, (prompt, image) in enumerate(zip(prompts, images)):
        max_retry = 5
        retry = 0
        while retry < max_retry:
            try:
                print("bard asking image {}".format(idx))
                bard_response = bard.ask_about_image(prompt, image)['content']    
                print(bard_response)
                bard_response = bard_response.split("\n")
                bard_response = [line.lower() for line in bard_response]
                responses.append(extract_anwser(bard_response))
                break
            except:
                print("retrying...")
                retry += 1
                if retry == max_retry:
                    responses.append(-1)  
        time.sleep(5)              

    return responses

if __name__ == "__main__":
    from prompt import env_prompts
    prompts = [env_prompts["CartPole-v1"]] * 2
    image1 = open("/media/yufei/42b0d2d4-94e0-45f4-9930-4d8222ae63e51/yufei/projects/vlm-reward/test_image/images_2023-12-03-22-43-17/000000.png", 'rb').read()
    image2 = open("/media/yufei/42b0d2d4-94e0-45f4-9930-4d8222ae63e51/yufei/projects/vlm-reward/test_image/images_2023-12-03-22-43-17/000001.png", 'rb').read()
    images = [image1, image2]
    responses = bard_query_session(prompts, images)
    print(responses)
