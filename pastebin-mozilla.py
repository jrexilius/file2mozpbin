# Simple pastebin client for Mozilla hosted service

import sys
import requests

# get data to post from file
try:
  post_file = sys.argv[1]
  post_data = ''
  fp = open(post_file,'r')
  post_data = str(fp.read())
  fp.close()
except Exception as e:
  print('post_data input error:',str(e))
  sys.exit(1)

# hit URL to get required token and cookie
post_url = 'https://pastebin.mozilla.org/'
try:
  response = requests.get(post_url,timeout=30)
except Exception as e:
  print('get session page error:',str(e))
  sys.exit(1)

# parse response
try:
  cookie_value = ''
  token = ''
  cookie_str = str(response.headers['Set-Cookie'])
  cookie_parts = cookie_str.split(';')
  (name,cookie_value) = str(cookie_parts[0]).split('=')
  token_str = ''
  for line in response.text.split("\n"):
    if 'csrfmiddlewaretoken' in line:
      token_str = line
  if token_str:
    token_str = token_str.replace('"','')
    token_str = token_str.replace('>','')
    parts = token_str.split('=')
    token = parts[3] 
except Exception as e:
  print('parse response error',str(e))
  sys.exit(1)

# construct post and headers
cookies = {}
cookies['csrftoken'] = cookie_value

headers = {}
headers['Referer'] = 'https://pastebin.mozilla.org/'

body = {}
body['csrfmiddlewaretoken'] = token
body['lexer'] = '_text'
body['expires'] = '86400'
body['rtl'] = ''
body['content'] = post_data

# post to service
try:
  response = requests.post(post_url,headers=headers,cookies=cookies,data=body,timeout=30)
except Exception as e:
  print('post to pastebin failed:',str(e))
  sys.exit(1)

# parse redirect history for ephemeral URL
final_url = ''
if response.history:
  for resp in response.history:
    if 'Location' in resp.headers:
      final_url = post_url[:-1]
      final_url+= str(resp.headers['Location'])

# print result, exit clean
print(final_url)
sys.exit(0)
