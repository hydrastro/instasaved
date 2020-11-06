import json
import time
from instagram_private_api import Client, ClientCompatPatch

# Bootstrap code
cookies = None
try:
  with open("cookies.pkl", "rb") as read_cookies:
    cookies = read_cookies.read()
except:
  pass

user_name = ""
password = ""

if cookies is None:
  print("not using cookies")
  api = Client(user_name, password, auto_patch=True)
else:
  print("using cookies")
  api = Client(user_name, password, cookie=cookies, auto_patch=True)

cookies = api.cookie_jar.dump()
with open("cookies.pkl", "wb") as save_cookies:
    save_cookies.write(cookies)


photo_urls = []

def parse_results(results):
  for result in results["items"]:
    try:
      carousel_imgs = result["media"]["carousel_media"]
      # print("have carousel media")
      for img in carousel_imgs:
        try:
          photo_urls.append(img["videos"]["standard_resolution"]["url"])
        except KeyError as e:
          photo_urls.append(img["images"]["standard_resolution"]["url"])
    except KeyError as e:
      # print("dont have it")
      try:
        photo_urls.append(result["media"]["videos"]["standard_resolution"]["url"])
      except KeyError as e:
        photo_urls.append(result["media"]["images"]["standard_resolution"]["url"])

results = api.saved_feed()
# print(json.dumps(results["items"]))
parse_results(results)
next_max_id = results.get('next_max_id')

print("sleeping for 1.5 seconds, next max id is: " + str(next_max_id))
time.sleep(1.5)

while next_max_id:
  results = api.saved_feed(max_id=next_max_id)
  parse_results(results)
  next_max_id = results.get('next_max_id')

  with open("urls.txt", "a") as myfile:
    for url in photo_urls:
      myfile.write(url + "\n")
  photo_urls = []

  print("sleeping for 1.5 seconds, next max id is: " + str(next_max_id))
  time.sleep(1.5)
