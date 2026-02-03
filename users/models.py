from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Default S3 image URL
DEFAULT_PROFILE_IMAGE_URL = 'https://know-me-media.s3.ap-south-1.amazonaws.com/profile_pics/default.jpg'

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.jpg',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def image_url(self):
        """
        Returns the S3 URL of the profile image, or the default image URL
        if no image has been uploaded.
        """
        # Check if user has uploaded their own image
        # If image field is empty/None, return default
        if not self.image or not self.image.name:
            return DEFAULT_PROFILE_IMAGE_URL
        
        # Check if it's the default placeholder path
        image_name = self.image.name.lower()
        # Treat any default.jpg (with or without folder) as the placeholder
        if image_name.endswith('default.jpg'):
            return DEFAULT_PROFILE_IMAGE_URL
        
        # User has uploaded a custom image, use it
        try:
            return self.image.url
        except:
            # Fallback to default if URL generation fails
            return DEFAULT_PROFILE_IMAGE_URL

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)