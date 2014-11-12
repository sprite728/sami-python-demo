from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Profile class model. Used to save the oauth access token for a user. """

    user = models.ForeignKey(User)
    oauth_token = models.CharField(max_length=200) #access token for user