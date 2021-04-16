from pusher_push_notifications import PushNotifications

class NotificationHelper:

    def sendNotification(self, email):
        beams_client = PushNotifications(
            instance_id='7032df3e-e5a8-494e-9fc5-3b9f05a68e3c',
            secret_key='8AC9B8AABB93DFE452B2EFC2714FCF923841B6740F97207F4512F240264FF493',
        )

        response = beams_client.publish_to_interests(
        interests=[email.replace('.', '')],
        publish_body={
            'apns': {
            'aps': {
                'alert': {
                'title': 'choose2reuse',
                'body': 'One of your conatiners has been verified as returned!', 
                },
            },
            },
            'fcm': {
            'notification': {
                'title': 'choose2reuse',
                'body': 'One of your conatiners has been verified as returned!',
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
        print('success', response['publishId'])
