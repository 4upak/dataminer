import requests
from bs4 import BeautifulSoup
import lxml
import time
from tqdm import tqdm
from database import Base,session,engine

s = requests.Session()
# all cookies received will be stored in the session object
#s.post('http://www...',data=payload)
source = s.get('https://www.olx.ua/d/obyavlenie/devochka-krasotka-IDNzCxV.html#09eaa5e1f8;promoted')

print(s.cookies.get_dict())

'''
:authority: www.olx.ua
:method: GET
:path: /api/v1/offers/732530120/limited-phones/
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: ru
authorization: Bearer 85143c822148763a338e881bcfaa7a740a6128d4
cookie: __gads=ID=512f6a3bd40f461e:T=1637321089:S=ALNI_MbgsPW-hHg9FnBAJg8htIBQmAT31A;
__gfp_64b=OwK8TDaO8MaVK2Eth9lUsFomykYY5JAI2gMIA_e_7xP.P7|1637321091;
__utma=250720985.1322686399.1637321090.1637753713.1639999606.3;
__utmc=250720985;
__utmz=250720985.1637684450.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);
_gcl_au=1.1.253171946.1637321091;
_gid=GA1.2.1966906549.1639999606;
_hjAbsoluteSessionInProgress=0;
_hjid=9daf839f-34c7-4e4e-9e20-e2a9484d6ba2;
_hjSession_2218922=eyJpZCI6IjA3ZDY5YjMxLTM0NjUtNGRkMC1hODQ4LWMzODNkZmVhNTAzYiIsImNyZWF0ZWQiOjE2Mzk5OTk2MDYxNTh9;
_hjSessionUser_1617300=eyJpZCI6IjlmNDFhM2RkLTlmMTEtNWUxNS05YTAxLTE4ZmQwNjQxMGQ3YiIsImNyZWF0ZWQiOjE2Mzc2ODQ1MDc4NjcsImV4aXN0aW5nIjp0cnVlfQ==;
_hjSessionUser_2218922=eyJpZCI6ImIxYmNhZjI5LTViNWEtNWYwOS1hODA4LTBkOTg5MWFjNGNlYiIsImNyZWF0ZWQiOjE2MzczMjEwODgwNDYsImV4aXN0aW5nIjp0cnVlfQ==;
a_access_token=85143c822148763a338e881bcfaa7a740a6128d4;
a_grant_type=device;
a_refresh_token=54358efbf95b8376f606773f766e4965711f3d3e;
cookieBarSeen=true;
cookieBarSeenV2=true;
dfp_segment=%5B%5D;
fingerprint=MTI1NzY4MzI5MTs4OzA7MDswOzE7MDswOzA7MDswOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTswOzE7MTsxOzE7MDswOzA7MDswOzA7MTsxOzE7MTsxOzA7MTswOzA7MTsxOzE7MDswOzA7MDswOzA7MDswOzE7MDswOzA7MDsxOzE7MTsxOzE7MDsxOzE7MTsxOzA7MTswOzI4MDU1MzEyODM7MjsyOzI7MjsyOzI7NTsyODQ4MDA2NDE4OzEzNTcwNDE3Mzg7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzA7MDswOzMzOTMxNTk2NTszNDY5MzA2NTUxOzM1NzY1MTk1OTg7MzMwODM4ODQxOzM5NTU0NDg2OTM7MjU2MDsxNDQwOzI0OzI0OzE4MDsxMjA7MTgwOzEyMDsxODA7MTIwOzE4MDsxMjA7MTgwOzEyMDsxODA7MTIwOzE4MDsxMjA7MTgwOzEyMDsxODA7MTIwOzE4MDsxMjA7MDswOzA=;
from_detail=0;
lang=ru;
laquesisff=euonb-114#euonb-48#kuna-307#oesx-645#oesx-867#olxeu-29763#srt-1289#srt-1346#srt-1348#srt-1593#srt-477#srt-479#srt-682;# laquesissu=219@map-click-fakedoor|0;
ldTd=true; 
lister_lifecycle=1637684448; 
mobile_default=desktop; 
observed_aui=20953e379e4d4503ad94fca84d65901b; 
PHPSESSID=129dbcbtcp1hsj78flrsq8h30d; 
sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; 
sbjs_current_add=fd%3D2021-12-20%2013%3A33%3A10%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.ua%2Fd%2Fobyavlenie%2Fzimniy-termo-kombinezon-lenne-IDM6Qx1.html%3Fsd%3D1%23ebec54ca7f%3Bpromoted%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.ua%2Fdetskiy-mir%2Fdetskaya-odezhda%2F; 
sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first_add=fd%3D2021-12-20%2013%3A33%3A10%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.ua%2Fd%2Fobyavlenie%2Fzimniy-termo-kombinezon-lenne-IDM6Qx1.html%3Fsd%3D1%23ebec54ca7f%3Bpromoted%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.ua%2Fdetskiy-mir%2Fdetskaya-odezhda%2F; 
sbjs_migrations=1418474375998%3D1; 
sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_14_6%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F96.0.4664.110%20Safari%2F537.36; 
user_business_status=private; 
user_id=736036145; 
x-device-id=l94anjwdqnjnhy%3A1637684501031; 
__diug=true; 
deviceGUID=e094fa02-c145-4ce5-98b0-b438be47a4ed; 
dfp_user_id=3708a84b-5f09-45e9-aa40-7fd856b45402-ver2; 
disabledgeo=1; 
laquesis=buy-1750@b#buy-2111@a#er-1205@a#erm-558@c#erm-567@c#jobs-2587@a#jobs-2959@b#oesx-1158@c#oesx-1159@b#srt-1517@b; 
_hjIncludedInSessionSample=0; 
user_adblock_status=false; 
search_id_md5=b907613f6e78b7f686cba5a3b8abbb44; 
__utmb=250720985.33.10.1639999606; 
lqstatus=1640008087|17dd7980b7bx5b13c910|jobs-2587#oesx-1159#buy-1750#er-1205||; 
newrelic_cdn_name=CF; 
_gat_clientNinja=1; 
cto_bundle=xV4oNV9ZJTJGMHdhZ1owWGxpOGVrNFpsbDI0TVZkdHJKS0xTQWtRRnlFcVlMeHVQeG94enowSUlxJTJCRlROOHc1UEQ1bXE3eEppTDVqUGcweHdkWVglMkZ0SXNjcUxvV1FPVDZqRXIwbEZSJTJGOEs4VnhqWnlzQnVveHdmOFNPQmdCWHhuNHJSUmZ0ZnAxYWh5U0pRSnNQSDhva3Z6M3JFcWdmSGtDbDVheU1lbjZ2ZFZZazltVEM2RmFRSVNsVkFtWGZHN3lCZmpzcA; 
store.test=; 
_ga=GA1.1.1322686399.1637321090; 
sbjs_session=pgs%3D40%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.olx.ua%2Fd%2Fobyavlenie%2Fdevochka-krasotka-IDNzCxV.html%2309eaa5e1f8%3Bpromoted; 
session_start_date=1640008770800; 
onap=17d37f11832x1b27e0a3-6-17dd7980b7bx5b13c910-212-1640008771; 
_ga_QFCVKCHXET=GS1.1.1639999606.5.1.1640006970.41

if-none-match: "e892c219794637c4200e815913df58b8"
referer: https://www.olx.ua/d/obyavlenie/devochka-krasotka-IDNzCxV.html
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36
version: v1.19
x-client: DESKTOP
x-device-id: e094fa02-c145-4ce5-98b0-b438be47a4ed
x-platform-type: mobile-html5

'''

soup = BeautifulSoup(source.text, "lxml")
price =  soup.find("div", "css-dcwlyx").find('h3').text.strip()

id = soup.find("span", "css-9xy3gn-Text").text.strip()
id = id.split(" ")[1]
url = f'https://www.olx.ua/api/v1/offers/{id}/limited-phones/'

source = s.get(url)
print(source.text)
