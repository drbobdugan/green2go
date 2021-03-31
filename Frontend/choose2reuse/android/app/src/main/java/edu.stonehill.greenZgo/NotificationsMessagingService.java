package edu.stonehill.greenZgo;

import android.util.Log;

import com.google.firebase.messaging.RemoteMessage;
import com.pusher.pushnotifications.fcm.MessagingService;

public class NotificationsMessagingService extends MessagingService {

    public NotificationsMessagingService() {
        super();
        Log.i("NotificationsSevice", "starting....");
    }

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.i("NotificationsService", "Got a remote message 🎉");
    }
}