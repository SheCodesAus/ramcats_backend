from django.db import models
from django.contrib.auth import get_user_model

class Eligibility(models.Model):
    description = models.CharField(max_length=500)

class Discipline(models.Model):
    description = models.CharField(max_length=500)

class Type(models.Model):
    description = models.CharField(max_length=500)

class Opportunity(models.Model):
    title = models.CharField(max_length=5000)
    description = models.TextField(blank=False)
    opportunity_url = models.URLField(max_length=200, blank=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_open = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    open_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
    close_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
    
    
    ONLINE = "ONLINE"
    FACE_TO_FACE = "FACE_TO_FACE"

    ATTENDENCE_MODE_CHOICES = [
    (ONLINE, "Online"),
    (FACE_TO_FACE, "Face to Face"),]

    attendence_mode = models.CharField(
        max_length=20,
        choices=ATTENDENCE_MODE_CHOICES
    )

    AUSTRALIAN_CAPITAL_TERRITORY = "ACT"
    NEW_SOUTH_WALES = "NSW"
    NORTHERN_TERRITORY = "NT"
    QUEENSLAND = "QLD"
    SOUTH_AUSTRALIA = "SA"
    TASMANIA = "TAS"
    VICTORIA = "VIC"
    WESTERN_AUSTRALIA = "WA"

    STATES_CHOICES = [
        (AUSTRALIAN_CAPITAL_TERRITORY, "Australian Capital Territory"),
        (NEW_SOUTH_WALES, "New South Wales"),
        (NORTHERN_TERRITORY, "Northern Territory"),
        (QUEENSLAND, "Queensland"),
        (SOUTH_AUSTRALIA, "South Australia"),
        (TASMANIA, "Tasmania"),
        (VICTORIA, "Victoria"),
        (WESTERN_AUSTRALIA, "Western Australia"),
    ]

    location = models.CharField(
        max_length=3,
        choices=STATES_CHOICES,
        default=WESTERN_AUSTRALIA
    )

    eligibility = models.ManyToManyField(Eligibility, related_name="opportunities")
    discipline = models.ManyToManyField(Discipline, related_name="opportunities")
    type = models.ManyToManyField(Type, related_name="opportunities")

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_opportunities')

    def clean(self):
        if self.study_mode:
            self.study_mode = self.study_mode.upper()
        if self.status:
            self.status = self.status.upper()
        super().clean()