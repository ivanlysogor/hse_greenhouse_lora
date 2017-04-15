import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

s=r.get("devices/lora/807B859020000001/lmt01")
# print s

data_array=s.split("/")

#print data
for data in data_array:
    try:
        datajson=json.loads(data)
        print datajson['status']['date']
        print datajson['data']['s1']
        print "\n"
    except:
        pass
# data=json.loads('{ "data": { "s1": -12.9, "s2": -12.9, "s3": -12.9, "s4": -12.9 }, "status": { "devEUI" : "807B85902000017A", "rssi": -42, "temperature": -10, "battery": 3300, "date": "2017-04-13T17:13:26.890348Z" }}')
# print data
#data=json.loads(s)
#print data
