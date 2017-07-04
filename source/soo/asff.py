#import packages
import urllib3
import json

http = urllib3.PoolManager()
urls = 'http://score.sports.media.daum.net/planus/do/v2/api/sports_games.json?category=kbo&date=20170702'

asdf = http.request('GET', urls)

x = json.loads(asdf.data.decode('utf-8'))
print(x)