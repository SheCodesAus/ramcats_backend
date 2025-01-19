from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    organisation = models.ForeignKey(
        'Organisation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    ORGANISATION = "Organisation"
    APPLICANT  = "Applicant"

    USER_TYPE_CHOICES = [(ORGANISATION, "Organisation"),(APPLICANT, "Applicant"),]

    user_type = models.CharField(
        max_length=100,
        choices=USER_TYPE_CHOICES,
        default=ORGANISATION
    )

    def clean(self):
        # TODO: ADD additional logic to user_type == applicant
        if self.user_type == self.ORGANISATION and not self.organisation:
            raise ValidationError("Organisations must have an associated organisation.")
        super().clean()

    def __str__(self):
        return self.username

class Organisation(models.Model):
    name = models.CharField(max_length=500)
    logo = models.URLField(blank=False)
    website = models.URLField(blank=False)
    description = models.TextField(blank=False)

    def __str__(self):
        return self.name