import requests
from requests.auth import HTTPBasicAuth
import sys
import datetime


# vidu_server = https://vidu.com
vidu_server = sys.argv[1]
# last_hour = 72
vidu_secret = sys.argv[2]
# last_hour = 72
last_hour = int(sys.argv[3])
vidu_get_session_url = vidu_server+'/openvidu/api/sessions'
vidu_user = 'OPENVIDUAPP'

r = requests.get(vidu_get_session_url, auth=HTTPBasicAuth(
    vidu_user, vidu_secret), verify=False)
data = r.json()


def to_last_x_hour(_now, _hour):
    return _now-(_hour*60*60*1000)


now = int(datetime.datetime.now().timestamp()*1000)


def epoch_to_date(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time)


filter_date = to_last_x_hour(now, last_hour)

for item in data['content']:
    sessionId = item['sessionId']
    createdAt = item['createdAt']
    if createdAt < filter_date:
        print(createdAt)
        requests.delete(vidu_get_session_url+'/'+sessionId,
                        auth=HTTPBasicAuth(vidu_user, vidu_secret), verify=False)
        
