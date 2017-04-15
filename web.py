import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

s=r.get("devices/lora/807B859020000001/lmt01")

data_array=s.split("/")

for data in data_array:
    try:
	    datajson=json.loads(data)
        print datajson['status']['date']
        print datajson['data']['s1']
        print "\n"
    except:
        pass
        
