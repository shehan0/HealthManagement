from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DIETITIAN = "DIETITIAN", "Dietitian"

    role = models.CharField(max_length=50, choices=Role.choices)

    @property
    def is_dietitian(self):
        return self.role == self.Role.DIETITIAN

    @property
    def is_approved_dietitian(self):
        if self.is_dietitian:
            return self.dietitian.is_approved
        return False


class Dietitian(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    country_of_practice = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    max_locations = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update the approval status of associated practice locations
        if not self.is_approved:
            self.locations.update(is_approved=False)


class PracticeLocation(models.Model):
    dietitian = models.ForeignKey(Dietitian, on_delete=models.CASCADE, related_name='locations')
    address = models.TextField()

    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Address: {self.address}, "f"Email: {self.email}, "f"Phone Number: {self.phone_number}, "f"Website: {self.website} "

    def save(self, *args, **kwargs):
        # Update the approval status of associated practice locations
        if self.is_approved and not self.dietitian.is_approved:
            raise ValidationError("Cannot approve a practice location if the associated dietitian is not approved.")

        # Limit max no of locations (It has been already handled in the template but this is for admin users actions)
        if not self.pk and self.dietitian.locations.count() >= self.dietitian.max_locations:
            raise ValidationError("Maximum of practice locations allowed reached.")

        super().save(*args, **kwargs)