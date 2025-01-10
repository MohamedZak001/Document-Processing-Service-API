import os
from PIL import Image

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model




def image_upload_path(instance: 'ImageFile', filename) -> str:
    return f"users/{instance.user.id}/images/{filename}"


class ImageFile(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="image_files")
    image = models.ImageField(upload_to=image_upload_path)
    uploaded_at =  models.DateTimeField(default=timezone.now, editable=False)

    @property
    def location(self):
        return self.image.path

    @property
    def width(self):
        if not hasattr(self,"_width"):
            self.read_image_meta_data()
        return self._width

    @property
    def height(self):
        if not hasattr(self,"_height"):
            self.read_image_meta_data()
        return self._height

    @property
    def number_of_channels(self):
        if not hasattr(self,"_number_of_channels"):
            self.read_image_meta_data()
        return self._number_of_channels
        
    def read_image_meta_data(self):
        with Image.open(self.image) as img:
            self._width = img.width
            self._height = img.height
            self._number_of_channels = len(img.getbands())
    

    def delete(self, *args, **kwargs):

        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
