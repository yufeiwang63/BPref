from bardapi import Bard
import requests
import time

token = 'dwj7Zvi4nOeBl6cxdL_bgDjl35xkgWnsq587pEHzf4drVppZOanlyhnpBtwZKngeJhgrQQ.'
bard = Bard(token=token)
res = bard.get_answer("what is google bard")['content']
print(res)
