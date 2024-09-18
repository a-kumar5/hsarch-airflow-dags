import apprise


class NotificationSender:
    def __init__(self):
        self.apprise = apprise.Apprise()

    def add_notification_service(self, url: str):
        """
        Add a notification service by URL.
        For example, Slack, Discord, Email, etc.
        :param url: Apprise URL for the service (e.g., 'mailto://user:pass@gmail.com', 'slack://token')
        """
        try:
            self.apprise.add(url)
            print(f"Successfully added service: {url}")
        except Exception as e:
            print(f"Error adding service: {e}")

    def send(self, title: str, body: str, notify_type: apprise.NotifyType = apprise.NotifyType.INFO):
        """
        Send the notification.
        :param title: Notification title
        :param body: Notification body
        :param notify_type: Notification type (info, success, warning, or failure)
        """
        try:
            self.apprise.notify(
                title=title,
                body=body,
                notify_type=notify_type,
            )
            print(f"Notification sent: {title}")
        except Exception as e:
            print(f"Error sending notification: {e}")


if __name__ == "__main__":
    # Initialize NotificationSender
    notifier = NotificationSender()

    # Add notification services
    # You can add multiple services here
    notifier.add_notification_service('workflows://prod-167.westus.logic.azure.com:443/3125ee3b2c8a4a4fa2f8e296f8086af6/xOQiMb74BbGS7xmWgGsZSqw-lRtRMbuhCXPycSBcM-4')
    notifier.add_notification_service('workflows://prod-167.westus.logic.azure.com:443/3125ee3b2c8a4a4fa2f8e296f8086af6/xOQiMb74BbGS7xmWgGsZSqw-lRtRMbuhCXPycSBcM-4/?template=template.json&:target=Chris&:whence=this%20afternoon')

    # Send a notification
    notifier.send(
        title="Deployment Successful",
        body="The new version of the app has been successfully deployed!",
        notify_type=apprise.NotifyType.SUCCESS
    )

apprise