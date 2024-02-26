from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
import os
from django.contrib.auth.hashers import make_password

def validate_picture_size(value):
    max_size = 1024 * 1024     # Max size in bytes (1MB)
    if value.size > max_size:
        raise ValidationError(f"Max file size is {max_size} bytes")
    
def validate_picture_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file format. Please upload a JPEG, PNG, or SVG file.')

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=150, blank=False)
    dob = models.DateField(blank=False)
    role = models.CharField(max_length=150, blank=False)
    mobile_number = models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True)
    profile_photo = models.ImageField(upload_to='images/', validators=[validate_picture_size, FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg'])], blank=True)

    def save(self, *args, **kwargs):
        # Check if the password has changed or it's a new record
        if self.pk is None or self._state.adding or self.password != self.confirm_password:
            # Hash the password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
             