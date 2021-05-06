from pusher_push_notifications import PushNotifications
import sys
import os
import datetime
sys.path.insert(0, os.getcwd()+'/databaseDAOs/')
from relationshipDAO import RelationshipDAO


need_to_be_messaged = []
relationshipDao = RelationshipDAO()
all_containers = relationshipDao.selectAll()[1]
containerList = []
for item in all_containers:
    containerDic = item.relationshipToDict()
    containerList.append(containerDic)
biggestSeen = 1
batch = [[]]
keys = {}
for x in containerList:
    if x['status']=='Checked Out':
      timeobj=datetime.datetime.strptime(x["statusUpdateTime"], '%Y-%m-%d %H:%M:%S')
      hours_added = datetime.timedelta(minutes= 5)
      future_date_and_time = timeobj + hours_added
      # it has been over 48 hours
      if (datetime.datetime.now() > future_date_and_time):
        if x['email'] in keys:
            keys[x['email']] += 1
        else:
            keys[x['email']] = 1
        if keys[x['email']] > biggestSeen:
            biggestSeen += 1
            batch.append([])
        need_to_be_messaged.append(x['email'])
for i in range(len(need_to_be_messaged)):
  need_to_be_messaged[i] = need_to_be_messaged[i].replace('.', '')

beams_client = PushNotifications(
    instance_id='7032df3e-e5a8-494e-9fc5-3b9f05a68e3c',
    secret_key='8AC9B8AABB93DFE452B2EFC2714FCF923841B6740F97207F4512F240264FF493',
)

for key in keys:
    for i in range(0, keys[key]):
        batch[i].append(key)

for b in batch:
    response = beams_client.publish_to_interests(
        interests=b,
        publish_body={
            'apns': {
                'aps': {
                    'alert': {
                        'title': 'choose2reuse',
                        'body': 'You have a container that has been checked out for over 48 hours... Please consider returning it...', 
                    },
                },
            },
            'fcm': {
                'notification': {
                    'title': 'choose2reuse',
                    'body': 'You have a container that has been checked out for over 48 hours... Please consider returning it...',
                },
            },
            'web': {
                'notification': {
                    'title': 'Hello',
                    'body': 'Hello, world!',
                },
            },
        },
    )
    print(response['publishId'])
