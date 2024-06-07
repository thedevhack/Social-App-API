from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

FRIENDSHIP_STATUS = {
    "Pending": "Pending",
    "Accepted": "Accepted",
    "Rejected": "Rejected"
}


class Friends(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_request_sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_request_received")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.CharField(max_length=50, choices=FRIENDSHIP_STATUS, default="Pending")
