from bardapi import Bard
import requests
import time

# token = 'dwj7Zj6bifYrS36NWnFQ6_noPEEiIb-lwi5GmTysg3MuvcxtsKaEyu9CZ8_zRZHpcTsJYw.'
# bard = Bard(token=token)
# res = bard.get_answer("what is google bard")['content']
# print(res)

import browser_cookie3

def find_cookie(cookie, field):
    for i in cookie:
        if(i.name == field):
            return i.value

session = requests.Session()

while True:
    cookies = browser_cookie3.chrome(domain_name='google.com')
    PPSID = find_cookie(cookies, '__Secure-1PSID')
    DCC = find_cookie(cookies, '__Secure-1PSIDCC')
    DTS = find_cookie(cookies, '__Secure-1PSIDTS')
    token = PPSID
    print(token)
    session.cookies.set("__Secure-1PSID", PPSID)
    session.cookies.set( "__Secure-1PSIDCC", DCC)
    session.cookies.set("__Secure-1PSIDTS", DTS)
    time.sleep(120)
