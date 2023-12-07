from bardapi import Bard, SESSION_HEADERS
import os
import requests
from vlms.copilot_infer import extract_anwser
import time, datetime

os.environ['_BARD_API_KEY'] = 'dwj7Zvi4nOeBl6cxdL_bgDjl35xkgWnsq587pEHzf4drVppZOanlyhnpBtwZKngeJhgrQQ.'
global bard, session

session = requests.Session()
token = os.environ['_BARD_API_KEY']
session.cookies.set("__Secure-1PSID", token)
session.cookies.set( "__Secure-1PSIDCC", "-")
session.cookies.set("__Secure-1PSIDTS", "-")
session.headers = SESSION_HEADERS
bard = Bard(token=token, session=session, timeout=30)


def background_refresh():
    global bard, session
    while True:
        try:
            new_cookies = bard.update_1PSIDTS()
            for str in ["__Secure-1PSIDTS", "__Secure-1PSIDCC", "__Secure-3PSIDTS"]:
                if new_cookies.get(str) is not None:
                    session.cookies.set(str, new_cookies.get(str))
            print("updating bard cookies!!")
            print("updating bard cookies!!")
            print("updating bard cookies!!")
            print("updating bard cookies!!")
            print("updating bard cookies!!")
        except:
            print("unable to update bard cookies!!")
            print("unable to update bard cookies!!")
            print("unable to update bard cookies!!")
            print("unable to update bard cookies!!")
            print("unable to update bard cookies!!")

        bard = Bard(token=token, session=session, timeout=30)
        time.sleep(60 * 6)
        
import threading
background_thread = threading.Thread(target=background_refresh, daemon=True)
background_thread.start()

# def update_bard_cookie():
#     session = requests.Session()
#     token = os.environ['_BARD_API_KEY']
#     session.cookies.set("__Secure-1PSID", token)
#     session.cookies.set( "__Secure-1PSIDCC", "-")
#     session.cookies.set("__Secure-1PSIDTS", "-")
#     session.headers = SESSION_HEADERS
#     bard = Bard(token=token, session=session, timeout=30)
#     try:
#         new_cookies = bard.update_1PSIDTS()
#         for str in ["__Secure-1PSIDTS", "__Secure-1PSIDCC", "__Secure-3PSIDTS"]:
#             if new_cookies.get(str) is not None:
#                 session.cookies.set(str, new_cookies.get(str))
#         print("updated bard cookies!!")
#         print("updated bard cookies!!")
#         print("updated bard cookies!!")
#     except:
#         print("unable to update bard cookies!!")
#         print("unable to update bard cookies!!")
#         print("unable to update bard cookies!!")
#         pass

#     return bard

# global last_time, bard
# last_time = time.time()
# bard = update_bard_cookie()

def bard_query_session(prompts, images):
    # global last_time, bard
    # if time.time() - last_time > 60 * 6:
    #     last_time = time.time()
    #     bard = update_bard_cookie()

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
        time.sleep(3)              

    return responses

if __name__ == "__main__":
    from prompt import env_prompts
    prompts = [env_prompts["CartPole-v1"]] * 2
    image1 = open("/media/yufei/42b0d2d4-94e0-45f4-9930-4d8222ae63e51/yufei/projects/vlm-reward/test_image/images_2023-12-03-22-43-17/000000.png", 'rb').read()
    image2 = open("/media/yufei/42b0d2d4-94e0-45f4-9930-4d8222ae63e51/yufei/projects/vlm-reward/test_image/images_2023-12-03-22-43-17/000001.png", 'rb').read()
    images = [image1, image2]
    responses = bard_query_session(prompts, images)
    print(responses)
