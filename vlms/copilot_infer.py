import time
import asyncio
# from sydney import SydneyClient
import os
import re
# os.environ["BING_COOKIES"] = "Imported_MUID=3FA226B5155269251099370914AF68C2; MUID=1EC47F116F976CE905226C156EF56DA0; MUIDB=1EC47F116F976CE905226C156EF56DA0; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=8DD14E2E21A34B55B50388D763D0E9C6&dmnchg=1; MMCASM=ID=3BF7D5F9D9884524ACCE08CE53B6EE05; _UR=QS=0&TQS=0; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wNS0yMVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6Mn0=; MicrosoftApplicationsTelemetryDeviceId=cc4b0ae5-f793-4253-9100-a5e99592b91c; _tarLang=default=zh-Hans; _TTSS_IN=hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=; _TTSS_OUT=hist=WyJlbiIsInpoLUhhbnMiXQ==; EDGSRCHHPGUSR=CIBV=1.1254.8; _clck=mokgxf%7C2%7Cfh5%7C0%7C1429; cct=Cffb_urZdisAp0P6vNFAEsf6w3w5wHQZ-jEyMkhVIPTp92m17lwSJuyY8w7vOSN0L4iUkfVdxiaD1tbYKUBpBQ; MSFPC=GUID=e70ad6509bb94fb1b3dea2ddb5c3df0f&HASH=e70a&LV=202305&V=4&LU=1684780378140; _Rwho=u=d; ipv6=hit=1701640675060&t=6; ABDEF=V=13&ABDV=13&MRNB=1701638155760&MRB=0; USRLOC=HS=1&ELOC=LAT=40.42680358886719|LON=-79.92975616455078|N=Pittsburgh%2C%20Pennsylvania|ELT=2|&BLOCK=TS=230522182420&CLOC=LAT=40.426803462389394|LON=-79.92975287671699|A=733.4464586120832|TS=231203205757|SRC=W; SnrOvr=X=; BFBUSR=CMUID=1EC47F116F976CE905226C156EF56DA0; CSRFCookie=59876c44-3694-488f-843a-3bb5dbea30e7; SRCHUSR=DOB=20230501&T=1701636665000&POEX=W; _EDGE_S=SID=087B2440F0D2630617EB379CF1FB62DD; ANON=A=6097BF59D5B9BF78885612E3FFFFFFFF&E=1d20&W=1; NAP=V=1.9&E=1cc6&C=VDcmAYxa8JAkDybN4PdPVwmgZ9_R6PWdj73Mqgl4P0ukLLptpAib-g&W=1; PPLState=1; KievRPSSecAuth=FAB6BBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACJ+tGqHhwekCOAQEhlBIoOIGmoshckdK4xYFB4VFh83rnz0xLZD4sTZ53uenJ2Dh4Cg579A/uJOO7CgUjcf60guqRkH/2wbPXvEG8+ZVSfGx/ZjYyJhHAHR0zuFk8NS8b4mP7sIUmR/alKkMRWndjXZJGZo7KTANq1ZkqgZKM+TCW7NKO1e/9ZD3J6PzaHN+mzgy0gIfW2Dfs0DGeyGRmVku+nVFy90qFeXSHY4nHZBx16sm2t1u0yboc0IQ8hyQ214eYJdLHp86BU5ZuXfDczElgJlsVqGzuvqyR0dyUl+ORzc3lzNKACT04FQ5vHSU9OBK5P1pYWuMDq6v+vEZaQclvnWuSQRk1Y8ZDJuRPpkYoH8wZmaWQxwXydxao/XhLhY5WovKy4wLZW/jDQeQpFZNyZ2uB0gMHIYlQIFPN1qh55CeHSvtLbrJz6iUoq0mVtgiwxhykUCiwqLjDfUGR7UU9UW+zkbHB8dd1Ai9FL8pto3xR9gfFU/P9UlwdQiX0C+px7qfCXSVOIf7lKmRgXuU6iX2hsLG8bl0yOyhSuumvZHr0c7BzUzt86X1z4uhZ7doOZpwLTJhwlM1L2KgXfb7yUfvwhuMIm7Zt+z5NaDkUibunoiuVI39BGZY1ZnvX7lEzIdefQ0P241Rr8KfqGyEXFsSRNkW/QOTPFKKeGvX5ShjnXH73vhym7q73T3OHle/SofGAeeScKtELD6jTtnl8wH9JLueEavhVPwimwR4W4EWplK1yJgvSBPDIBtCCeIvxEoMBTA9mc/jDV2vSG1h9OcXN0Wa9ejTMy9/SwYcs176S5SCLNPAmgahwrckNbT80hM8s3faC6oORZLpkdgZtzOiO4aKBUL3fEDzJUuPZN89RjoYBtEvTP+4QNzKEpibxTvnFbB+Z0ZPiDvNk5N3Skqsrwr7+Z/TcU83tWVSWvKd8QKhXwpJTTAMUm52RmiBNdaVKnewTUVpvyCWaw0VxriUkAD8I78K6gEIZZDG0epNFPiFT2/sfEKblAKyDSgrmj5W0vRLUdsQUPAoY9RwO0/bijrFL8dcICBKgaOuEkplFSZHLdFEAI4bEIGy9DKa0ej87181Zhg79F2IhD518L1bXwkgHb4V7xvB79IVPv+QZ+DFbQBox5yUWEIaXdc9zQC+0HgtgUKlpSxIBwXbLe4voiJLRBqgiF/fwyaJdbXIQ+unL53d9jak+IdAwTPdYIAPguX/nqCupLxu3oF5EnBqwyUU2TT9tDhX0dlANiP+a5BsraVn1fW5f83oUk0+wSMJy0CR4b7K8DSccTR3U1O9zr2BmbQMLsSf+mZnqUVuXpuGoLdEKTpWinnVe6KJTB4wY+9d1TcQrqjfg2zUKWPqtAP0ayLifzglnCKTTKl8Q73HMvq3fMnJ1GQldzkVGHCsql82iGbgmNeTegvDQBD/6tMGB7SKwkHgJ/0NcR4UAAAj3wvPHrHgNPCHp/sWC/sVryHo; _U=16qSMB7EDPqPyfPPYyMhPLYgZHc9jI0Z0tsKP1T1myiCNcAR_M3OaTjct5KK7_-14xqJzxpdxFjsaD7KhDG2IzAB0964gzw0ZwkA7tUnp2hGJUmuYoGCbDRBwmR6uekhymu2VTOTjN5zTftZjikKXpuXv3NjSy2An5UpU3yUc7wx6xa4TbZYSZOVzCvsTDBZ4AvcM5kSqmwLnU_x3NaaxmifBP_2ABLc3XetKhggUJdU; WLS=C=ea871e4157671e93&N=Yufei; WLID=rw44oUF8Z+Rb44LDMp7MBBg3YyJVnteZ/C9dfVBlCD5Ki57U83gtnLzJWrnvXcImzdlN9WDjbP2cmyRDa4J4PwN075gmznnUUM4PsLhXyCI=; _SS=SID=03AD11994245680F2B05024543276974&R=0&RB=0&GB=0&RG=0&RP=5; _RwBf=W=1&r=0&ilt=1&ihpd=0&ispd=1&rc=0&rb=0&gb=0&rg=0&pc=5&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=2&l=2023-12-03T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=MSAAUTOENROLL&c=MR000T&t=2727&s=2023-12-03T06:39:17.7942180+00:00&ts=2023-12-03T21:37:21.6255810+00:00&rwred=0&wls=2&wlb=0&ccp=0&lka=0&lkt=0&aad=0&TH=&mta=0&e=9FVDjZULwYbT5dFl9Z47zae0IkH0AIEs0C6JnbKj4lbFjKK4Nmo-6zaIK650Un1cCrfHZcxPp6QPPcBweViFbc1xgUqiqOA4reak5uY3yVI&A=6097BF59D5B9BF78885612E3FFFFFFFF; GC=qbm6CY4PzW43iarEiCZWL5dbEPptk002ktN14mS2BPKvAdV8D7zBvirlm6i_l8Cof3UeJbHHD1c0ZgJFieRRTg; SRCHHPGUSR=CW=987&CH=958&SCW=1164&SCH=4532&BRW=HTP&BRH=M&HV=1701639444&SRCHLANG=en&DM=0&PRVCW=987&PRVCH=958&DPR=1.0&UTC=-300&PV=15.0.0&BZA=0&IG=86B033B069A5431B9AD2429DA33697BC&SPLSCR=1&CIBV=1.1381.4&EXLTT=14&cdxtone=Balanced&cdxtoneopts=,glfluxv15&CMUID=1EC47F116F976CE905226C156EF56DA0"
# os.environ["BING_COOKIES"] = "Imported_MUID=3FA226B5155269251099370914AF68C2; MC1=GUID=e70ad6509bb94fb1b3dea2ddb5c3df0f&HASH=e70a&LV=202305&V=4&LU=1684780378140; MUID=1EC47F116F976CE905226C156EF56DA0; _fbp=fb.1.1686707524470.443380163; USRLOC=HS=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=9B396AA937B84146926508F06B65F4B3&dmnchg=1; MSCC=NR; _clck=55kdig%7C2%7Cfh8%7C1%7C1251; _uetsid=ddcd726091a511ee9cb75d76e3f9f593; _uetvid=92a11960033c11eeaeb15d48a600f622; msresearch=%7B%22state%22%3A%7B%22name%22%3A%22IDLE%22%7D%2C%22userid%22%3A%2217015852073911380106231121256%22%7D; display-culture=en-US; mbox=PC#41e63f193f97482b871a50eec794095b.34_0#1735780858|session#587804b6598d4069898c11b1a900074f#1701596020; AMCV_EA76ADE95776D2EC7F000101%40AdobeOrg=1585540135%7CMCIDTS%7C19695%7CMCMID%7C36196686932194518024470805307340984657%7CMCAAMLH-1702198959%7C7%7CMCAAMB-1702198959%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCCIDH%7C-822442808%7CMCOPTOUT-1701601359s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19702%7CvVersion%7C4.4.0; MUIDB=1EC47F116F976CE905226C156EF56DA0; _EDGE_S=SID=08D301CB318C6A370E1D121730EB6B06; _Rwho=u=d; CSRFCookie=4c628738-d077-4a35-865a-9c352948dc82; SRCHUSR=DOB=20231130&POEX=W; ANON=A=6097BF59D5B9BF78885612E3FFFFFFFF&E=1d20&W=3; NAP=V=1.9&E=1cc6&C=b8buA-XiDqFPazV-x-zmc2lcxnCk9a1Q0Hu9DkHZf8qV8eqSUqKy4w&W=3; PPLState=1; KievRPSSecAuth=FAB6BBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACOod50EbsOnwOARVKx/8tnk11MomahQCdvMRVcJkx7IfI36ysTB11zIa5TnI6gJhbmJiyZL8+Tks0jX2fWrZyr9QRoggHWw8Z4UbHPzwcOW2VhyM1o+tP8RlyQp17RrRzKTMUDfgEuLs2SrmwFNZoKRaen+YDfJGo+ER76s+8K5oqXV88CQk8yj2l/PHrxaPM7ABNZ7zHXr3J9941/0i5ivknw+uHJD9PR+YukFzv0rlmplP/qvxVXTl7/z65foODp9kIsNfLIS/fyDefvg8AunBDWY6+uOCbJFjUXKHAwPfHyjbUCqLUVmwWhcH02CeDeFGx1GC3grfa4eg1xHfohgaWpz5/8mgmo9jjbPZEQqj44MVtstJaQEUTnjA/j4rtv/coaS7pKEXucuHeVbJt7I/UVZ3IzXdv8OfZ2UfsoNcyq6/kigJOcP+FI9PHXXBCI51F5kvLrQ/Qot4O2mQMwaGKTp4V5UAjffZcsdJyNgkGqqvGo6QKy9pf9PA9Bpxvr0awVpj12uUax8SmF54Qllw6/Ftsi/L0Zm1SPH/6WJjm5tACiDhFCr83dJVMhNkQYb63doBM3B7AMyYt1F7ifQSfG7beSTUknK2tt+oSUJcQXK/JHtctQV6sqnh9dQIrLQxHl5CtxOtKx13Ru3ipDf+lAy31Ju1OA8DMz38/eZgyBZfjawISleN2OJIq/LrcWwMfwP3xxy0J8avU3FTIZcebn7iZ/KB4/wHYKtycq/O4fycpl7odFZiJW4KEW6NoUvCWS8lV2oKCDug8z4+qHvwBXXtYIhgL+VTqsnCVBg74XDesIOhfQv0/K/bSiUcC3o7OfQtIaQvZGl1cAsr9tGxpAKFXwwV5QA/Sr8sFp2lL2DI8x2DMkB5ISwCN8tofrTrvueV/RuLU8KBsRHct9pY+kES5ED0JXhMGVqt3IxsnAHOf3To1EkTCI88Nr2NpA3xdCZmp2PwdaLOzd+uOQa3Oq7GMv4VXuQzMp63Cvf17WmsBpTICYXiODcWtNeIUfVduE6OiPsZLEpycV/NzaZ9bTHu2g0nzsEbp3O1oDM0VMvw8vUL9S5uINtwi0iEAeW3pNrugz6RhAwtr1jm/Gy+AynjVPUHIaVZOC8Z7R1Rm7dW0RFIU1MYYuKT+i33oKbNN7I/mel/pxdSgUptQJbBEngw1GHYV6DmCu+8FEudJm/rYXxXHmjEkQQh7hz1/2iCwd78blOmo9MzkD4aK5IB4y5mhuwpyprfD9QgcvngKaEU3+XE7WLGtGpkqmzB9EKsOAWYM+eVIQCv822HXbQYql2V+/ADCARhCg9oJF1WNRGAQYpRmtCK/lh13k0yfC7HZlOLJ2Dv9uizL7NhUXIZtMTpvwLOUcxbYeTpJ6mGJ75+R9C7J+rgGd8IYJF9X9gAg7Lp9wOmAMXPnL2TabH6ts/Rq63W3UJuZA6eFnPlIcQUAOkb8N8gv/l9stZEYC7eP9qWFAei; _U=1blXKmxG-MPFE0vP2oDjlpBkv0pruvfxX7oxpPjJ4VWsJ1V1TVf4UN8-8RisaI4NNbYX_J_ieIw0hW4R3YhYerSewcLAiJ79bpLv54iewyioKd81WRdf2iceGj1_eBijnGovuwkzk0a30p4my8kLc62mHhri6u85BCqYVbbnB-Pg7Vkgs5rhOpKBbTM6-XoSleAXOMzlnl-d2weKo_RVAxHnsSKEdWE9CB2s7XvPRdZg; WLS=C=ea871e4157671e93&N=Yufei; WLID=rw44oUF8Z+Rb44LDMp7MBBg3YyJVnteZ/C9dfVBlCD5Ki57U83gtnLzJWrnvXcImzdlN9WDjbP2cmyRDa4J4PwN075gmznnUUM4PsLhXyCI=; _SS=SID=08D301CB318C6A370E1D121730EB6B06&R=0&RB=0&GB=0&RG=0&RP=0; SnrOvr=X=; _RwBf=W=0&mta=0&rc=0&rb=0&gb=0&rg=0&pc=0&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=1&l=2023-12-03T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=MSAAUTOENROLL&c=MR000T&t=2727&s=2023-12-03T06:39:17.7942180+00:00&ts=2023-12-03T22:02:39.5409779+00:00&rwred=0&wls=2&wlb=0&ccp=0&lka=0&lkt=0&aad=0&TH=&e=9FVDjZULwYbT5dFl9Z47zae0IkH0AIEs0C6JnbKj4lbFjKK4Nmo-6zaIK650Un1cCrfHZcxPp6QPPcBweViFbc1xgUqiqOA4reak5uY3yVI&A=6097BF59D5B9BF78885612E3FFFFFFFF; SRCHHPGUSR=SRCHLANG=en&PV=15.0.0&BRW=HTP&BRH=M&CW=987&CH=958&SCW=987&SCH=958&DPR=1.0&UTC=-300&DM=0&PRVCW=1912&PRVCH=958&CIBV=1.1342.3-cplt.10&cdxtone=Balanced&cdxtoneopts=,glfluxv15"
os.environ["BING_COOKIES"] = "Imported_MUID=3FA226B5155269251099370914AF68C2; MUID=1EC47F116F976CE905226C156EF56DA0; MUIDB=1EC47F116F976CE905226C156EF56DA0; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=8DD14E2E21A34B55B50388D763D0E9C6&dmnchg=1; MMCASM=ID=3BF7D5F9D9884524ACCE08CE53B6EE05; _UR=QS=0&TQS=0; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wNS0yMVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6Mn0=; MicrosoftApplicationsTelemetryDeviceId=cc4b0ae5-f793-4253-9100-a5e99592b91c; _tarLang=default=zh-Hans; _TTSS_IN=hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=; _TTSS_OUT=hist=WyJlbiIsInpoLUhhbnMiXQ==; EDGSRCHHPGUSR=CIBV=1.1254.8; _clck=mokgxf%7C2%7Cfh5%7C0%7C1429; cct=Cffb_urZdisAp0P6vNFAEsf6w3w5wHQZ-jEyMkhVIPTp92m17lwSJuyY8w7vOSN0L4iUkfVdxiaD1tbYKUBpBQ; MSFPC=GUID=e70ad6509bb94fb1b3dea2ddb5c3df0f&HASH=e70a&LV=202305&V=4&LU=1684780378140; BFBUSR=CMUID=1EC47F116F976CE905226C156EF56DA0; USRLOC=HS=1&ELOC=LAT=40.42697525024414|LON=-79.929931640625|N=Pittsburgh%2C%20Pennsylvania|ELT=2|&BLOCK=TS=230522182420&CLOC=LAT=40.42697399110731|LON=-79.92993282025009|A=733.4464586120832|TS=231204072556|SRC=W; _Rwho=u=d; ipv6=hit=1701678508004&t=6; SnrOvr=X=; CSRFCookie=9ab4b534-5c6e-462f-a6e1-3662557a341f; SRCHUSR=DOB=20230501&T=1701674904000&POEX=W; _EDGE_S=SID=26BA018DA4AC6FA215FB1250A5B56EEC; ANON=A=6097BF59D5B9BF78885612E3FFFFFFFF&E=1d21&W=2; NAP=V=1.9&E=1cc7&C=Mb0FfuLZJX9CYcAmi8TiofYrSsLzTTdOEsztxu2t8e-c_SDZIUulGA&W=2; PPLState=1; KievRPSSecAuth=FAB6BBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACCu1cIYskv08OARBqINLHZh8tC83jlJntqcO4r6CcH618kdPtZod5ELuwBU5FUO/HTkVStNhU2IT8opdfVgOdX8J9ovVq4+XJp7n5J6g61JW/PVjDy6Wtf3wdWZSmyCfjfKIALZGm2dX8g+s0lb9/s1Ev4SLAX59nwrjiUX09qdMR7uFSVterysNo2QIfC1oDNq0DYWdEheCLMLyfrmVKRAMdW9eXGsxNdU1YoYhBGEOuyc9JUB7sjusNh2AM4E7sJiOyBUTj/5I6A84XETbEjFsbC0F2KT2iF9CVv/ZPUuP6NkrZYt2+9BKL0q/gSflvhNxlFcUrJRy1dKoTTX4+nk+CqKf1ZhzxHcbRC/n5K93ZBzgEXNl6vuS0yjEsEZ83C83oCgQUJT9f2EtjZ+kdxb9CKhduqw0OFpiPlMWQNCJ8qVeAqotlJcQQQef4vvBsoKAHtl/Weyw6Zi/oCVQBicDbp/Gho+IuGRVCAbcPzHsbGCO5Oz89yRSBbDODlJ6HN4nfSHi6/c/jTWkQciC5rADHZAOhAL8PpBTXUPVtWnLo5e70G8xQouNafwivrpeU0adJKmhzGY0clqETVGWmU9rfoGc+YVmVroinC00TLYc1+fLcOTSPRLfKyds9GU8+8+QPjt7AD1dzp7WsF1E5zhDLIM01TQjuqNF2UL4AsrRwT4KQtpDJ4KwWWaxlKfYsFqVGOPy9SJLq5BdhGhkIeQdx/0ycOs4HHwSRvGHmI05c41qKBhWMM71Cn6pEkYVhtRvq00QL1EBiQHotjb2qUW7QJ14Ip1liDOfuYiuOZQJQKjlWkN8nrghWX38o7p+pSPZqu6dIeiSYsMJiukv69I9m8NpQRTZ5jHFRovFpXDOJ5bAFkZHLm9YBdcHRGW3DGxdMMHZ+UZdTfmnIa9tTAekacbpDMYzW0GrCXlqgSEbxnL8t5u2u3IVEql9uX/x/VpX2FT4esaqSaAcywM/UVkgIYieD40nl2LAiTbOrudG/BEMmbW3YN9CDvrhCHBWrGwqmUDSlumLu8ivniJj4Drp1LlAfCoDlcARvO2VLInU2VSderes3h3aqr7nfU53EEy2f80RHmG7DWhk5yqJGfBSIVdqM3dAQx//8kBRvIEj74IAyQD+HLt0vyaLcnZiIV5QutBgNtwKCQaWtemtOX9CdIqwgIODKdh8oJgNzvvuzuhIudJDcuOX9f99xdWkC1Ol+qng8r6u7pb6U1fTucAgJ1BurE9GT/S7mlovzpYBbzUms9ZcEtO8MSuoB/xJ9RMo2HmtTG8LU0zw1hcHnCzgjaBn6RR0sNfH5YncjpEeoGq/axVDHQN9g4Nz6MiaFdWbiiqHT/8Za2sJ4cC5dDD9ggHG0SypubpPOqJ/UVKeZZP6vWbsXyfZeO0buXS7n7V57l9+wsT99kJAvtJ/+i5PhPg2tkKxC88MhsFwzNePUtkUAIHqqQEI07uQ8AfSzYL5byUnRvpe; _U=1miqDswVTsyU0Wv16Ngq32kOZQPWKsiL3-IuC9w_UefkzQ3MX0ZGBmXIggv7NALGkpFdQmJ3oVXmcVQwNDEmFJ9LRjLvtAazDlGKOd4w-HCZ-fFBx8KDqRQ3F_ulweFMmpyNmeFWs2KUcgH6Yh_BqcB4IvFt7xVcK8e7zzBGEAMvQU0W9u-2IfScfm4I8AgS2sIXHbdyNnZj6fWETZvxQJGTVCAMlJ7hxAI805o3PdHI; WLS=C=ea871e4157671e93&N=Yufei; WLID=rw44oUF8Z+Rb44LDMp7MBBg3YyJVnteZ/C9dfVBlCD5Ki57U83gtnLzJWrnvXcImzdlN9WDjbP2cmyRDa4J4PwN075gmznnUUM4PsLhXyCI=; ABDEF=V=13&ABDV=13&MRNB=1701675008862&MRB=0; _SS=SID=13F655AA0952656D34EC4677084B64EC&R=0&RB=0&GB=0&RG=0&RP=5; _RwBf=W=1&r=0&ilt=2&ihpd=0&ispd=2&rc=0&rb=0&gb=0&rg=0&pc=5&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=3&l=2023-12-03T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=MSAAUTOENROLL&c=MR000T&t=2727&s=2023-12-03T06:39:17.7942180+00:00&ts=2023-12-04T07:30:11.0440066+00:00&rwred=0&wls=2&wlb=0&ccp=0&lka=0&lkt=0&aad=0&TH=&mta=0&e=9FVDjZULwYbT5dFl9Z47zae0IkH0AIEs0C6JnbKj4lbFjKK4Nmo-6zaIK650Un1cCrfHZcxPp6QPPcBweViFbc1xgUqiqOA4reak5uY3yVI&A=6097BF59D5B9BF78885612E3FFFFFFFF; SRCHHPGUSR=CW=1111&CH=958&SCW=1164&SCH=4126&BRW=S&BRH=M&HV=1701675011&SRCHLANG=en&DM=0&PRVCW=1111&PRVCH=958&DPR=1.0&UTC=-300&PV=15.0.0&BZA=0&IG=1209B97B95134320AE055F99A0EDB499&SPLSCR=1&CIBV=1.1381.4&EXLTT=31&cdxtone=Balanced&cdxtoneopts=,glfluxv15&CMUID=1EC47F116F976CE905226C156EF56DA0&WTS=63837238949; GC=qbm6CY4PzW43iarEiCZWL5dbEPptk002ktN14mS2BPJHitm2xSctjrQYrw4lpLJaxSGDJjQZ4OGAS_FQYcJLsQ"

def extract_anwser(response):
    for line in response:
        match = re.search(r'output: (.*)', line)
        line = line.replace("*", " ")

        # Extracting the matched substring
        if match:
            extracted_string = match.group(1)
            if "left" in extracted_string.lower():
                print("vlm answer: left")
                return 0
            elif "right" in extracted_string.lower():
                print("vlm answer: right")
                return 1
    
    print("vlm answer: -1")
    return -1

async def fetch_response(prompts, attachments):
    responses = []
    async with SydneyClient() as sydney:
        for prompt, attachment in zip(prompts, attachments):
            response = await sydney.ask(prompt, attachment=attachment, citations=True)
            print(response)
            response = response.split("\n")
            response = [line.lower() for line in response]
            
            responses.append(extract_anwser(response))
            time.sleep(1)
            
    return responses

async def query(prompt, list_of_attachments):
    # Create a list of tasks
    tasks = [fetch_response([prompt for _ in range(len(attachments))], attachments) for attachments in list_of_attachments]

    # Run tasks concurrently
    responses = await asyncio.gather(*tasks)
    flat_responses  = [item for sublist in responses for item in sublist]
    return flat_responses

if __name__ == "__main__":
    import pickle as pkl
    text_prompt = """
There are two cartpoles in the image, one on the left, and one on the right.
They are both about the task of cartpole, where a pole is attached to a cart, and the goal is to balance the pole upright on the cart without falling down. The task is considered to be better achieved if the tilt angle of the pole is small from being vertical.
Please reply which of the two cartpoles you think better achieves the goal.
Think step by step.
Please first reply with your reasoning, and then followed by a single line with "output: left" or "output: right".

Example output format:
I think the left cartpole is better because it has a smaller tilt angle. [More reasoning here]
output: left
"""
    
    attachments = [
        ["https://raw.githubusercontent.com/yufeiwang63/test_image/main/images_2023-12-03-16-11-00/000000.png".format(i) for i in range(2)],
        # ["https://raw.githubusercontent.com/yufeiwang63/test_image/main/images_2023-12-03-16-11-00/000000.png".format(i) for i in range(2)]
    ]
    
    rewards = pkl.load(open("/media/yufei/42b0d2d4-94e0-45f4-9930-4d8222ae63e51/yufei/projects/vlm-reward/data/{}/rewards.pkl".format("CartPole-v1"), "rb"))
    
    
    start = time.time()
    preds = asyncio.run(query(text_prompt, attachments))
    end = time.time()
    print(end - start)
    
    success = 0
    for i in range(5):
        gt_label = 0 if rewards[i * 2] > rewards[i * 2 + 1] else 1
        print("image {} pred: {} gt: {}".format(i, preds[i], gt_label))
        success += (preds[i] == gt_label)
    
    print("success rate: {}".format(success / 10))
        
